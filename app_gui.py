import customtkinter as ctk
import datetime
import os
from fpdf import FPDF
from nutrition_data import (FOOD_LIBRARY, DAILY_DOZEN_TARGETS, NUTRITION_DATA, 
                            WEEKLY_TARGETS, FOOD_TIPS, get_best_sources, 
                            CONVERSION_FACTORS, SERVING_SIZES)

class MealPrepApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Daily Dozen Decision Engine")
        
        # Safe geometry for most laptop screens
        self.geometry("1400x750")
        
        # Track selections
        self.selected_items = {cat: ctk.StringVar(value="") for cat in FOOD_LIBRARY.keys()}
        self.bucket_widgets = {} 
        
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.setup_ui()

    def setup_ui(self):
        # Header
        ctk.CTkLabel(self, text="Weekly Hero Ingredient Selection", 
                     font=("Arial", 24, "bold")).grid(row=0, column=0, pady=20)

        # Left Side: Selection Buckets (Horizontal Scroll)
        self.scroll_frame = ctk.CTkScrollableFrame(self, orientation="horizontal")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        for category, items in FOOD_LIBRARY.items():
            frame = ctk.CTkFrame(self.scroll_frame, width=240)
            frame.pack(side="left", padx=10, fill="y")
            
            ctk.CTkLabel(frame, text=category, font=("Arial", 14, "bold"), 
                         text_color="#1f6aa5").pack(pady=5)
            
            s_var = ctk.StringVar()
            search_entry = ctk.CTkEntry(frame, placeholder_text="Search...", 
                                        textvariable=s_var, height=25)
            search_entry.pack(padx=10, pady=5, fill="x")
            s_var.trace_add("write", lambda *args, c=category, v=s_var: self.filter_buckets(c, v))

            rb_cont = ctk.CTkFrame(frame, fg_color="transparent")
            rb_cont.pack(fill="both", expand=True)
            
            self.bucket_widgets[category] = []
            for item in items:
                rb = ctk.CTkRadioButton(rb_cont, text=item, 
                                        variable=self.selected_items[category], 
                                        value=item, command=self.update_analysis)
                rb.pack(anchor="w", padx=15, pady=5)
                self.bucket_widgets[category].append(rb)

        self.setup_analysis_panel()

    def setup_analysis_panel(self):
        # Right Side Main Container
        self.right_sidebar = ctk.CTkFrame(self)
        self.right_sidebar.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)
        
        # Dashboard (Nutrient Progress)
        self.dashboard_frame = ctk.CTkScrollableFrame(self.right_sidebar, height=300)
        self.dashboard_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(self.dashboard_frame, text="Weekly Dashboard", font=("Arial", 18, "bold")).pack(pady=10)
        
        self.nut_widgets = {}
        for nut, target in WEEKLY_TARGETS.items():
            cont = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
            cont.pack(fill="x", padx=10, pady=2)
            h = ctk.CTkFrame(cont, fg_color="transparent"); h.pack(fill="x")
            lbl = ctk.CTkLabel(h, text=f"{nut.title()}: 0/{target}", font=("Arial", 11)); lbl.pack(side="left")
            ctk.CTkButton(h, text="Find", width=30, height=18, command=lambda n=nut: self.suggest_fix(n)).pack(side="right")
            bar = ctk.CTkProgressBar(cont); bar.set(0); bar.pack(fill="x")
            self.nut_widgets[nut] = {"label": lbl, "bar": bar}

        # Auditor Box (Expands to fill middle space)
        self.report_box = ctk.CTkTextbox(self.right_sidebar, font=("Courier New", 12))
        self.report_box.pack(pady=10, padx=10, fill="both", expand=True)

        # Action Buttons (Pinned to the bottom)
        self.button_area = ctk.CTkFrame(self.right_sidebar, fg_color="transparent")
        self.button_area.pack(side="bottom", fill="x", pady=10)

        self.list_btn = ctk.CTkButton(self.button_area, text="Generate Shopping List", 
                                       fg_color="#2ecc71", hover_color="#27ae60",
                                       command=self.display_shopping_list)
        self.list_btn.pack(pady=5, fill="x", padx=10)
        
        self.pdf_btn = ctk.CTkButton(self.button_area, text="PDF Export for Kitchen", 
                                     fg_color="#3498db", hover_color="#2980b9", 
                                     command=self.export_to_pdf)
        self.pdf_btn.pack(pady=5, fill="x", padx=10)

    def filter_buckets(self, category, s_var):
        query = s_var.get().lower()
        for rb in self.bucket_widgets[category]:
            if query in rb.cget("text").lower():
                rb.pack(anchor="w", padx=15, pady=5)
            else:
                rb.pack_forget()

    def suggest_fix(self, nut):
        top = get_best_sources(nut)
        msg = f"\n>>> TOP {nut.upper()} SOURCES <<<\n"
        for i, (n, v) in enumerate(top):
            msg += f"{i+1}. {n} ({v} per serving)\n"
        self.report_box.configure(state="normal")
        self.report_box.insert("1.0", msg + "-"*20 + "\n")
        self.report_box.configure(state="disabled")

    def update_analysis(self):
        totals = {n: 0 for n in WEEKLY_TARGETS}
        active_items = []
        for cat, var in self.selected_items.items():
            item = var.get()
            if item in NUTRITION_DATA:
                active_items.append(item)
                data = NUTRITION_DATA[item]
                servs = DAILY_DOZEN_TARGETS.get(cat, 1)
                for n in totals:
                    totals[n] += data.get(n, 0) * servs * 7
        
        for n, v in totals.items():
            target = WEEKLY_TARGETS[n]
            self.nut_widgets[n]["bar"].set(min(v/target, 1.0))
            self.nut_widgets[n]["label"].configure(text=f"{n.replace('_', ' ').title()}: {round(v,1)}/{target}")
            self.nut_widgets[n]["bar"].configure(progress_color="#2ecc71" if v >= target else "#3498db")
        
        report = self.generate_audit_report(totals, active_items)
        self.report_box.configure(state="normal")
        self.report_box.delete("1.0", "end")
        self.report_box.insert("1.0", report)
        self.report_box.configure(state="disabled")

    def generate_audit_report(self, totals, active):
        report = "=== SYNERGY AUDIT ===\n\n"
        if totals.get('iron', 0) < WEEKLY_TARGETS['iron'] and totals.get('vitamin_c', 0) > WEEKLY_TARGETS['vitamin_c']*1.5:
            report += "* SYNERGY: High Vitamin C detected! Boosting iron absorption.\n\n"
        if any(NUTRITION_DATA.get(x, {}).get('oxalate_high') for x in active):
            report += "! OXALATE WARNING: High-oxalate choice. Add Kale/Bok Choy for Calcium.\n\n"
        report += "--- PREP SECRETS ---\n"
        for item in active:
            if item in FOOD_TIPS:
                report += f"- {item}: {FOOD_TIPS[item]}\n"
        return report

    def display_shopping_list(self):
        msg = "=== WEEKLY SHOPPING LIST ===\n\n"
        for cat, var in self.selected_items.items():
            item = var.get()
            if item:
                needed = DAILY_DOZEN_TARGETS.get(cat, 1) * SERVING_SIZES.get(cat, 100) * 7
                qty = needed / CONVERSION_FACTORS.get(item, 1.0)
                unit = "g" if qty < 1000 else "kg"
                val = qty if qty < 1000 else qty / 1000
                msg += f"[ ] {item}: {round(val, 2)}{unit} (Dry/Raw weight)\n"
        self.report_box.configure(state="normal")
        self.report_box.delete("1.0", "end")
        self.report_box.insert("1.0", msg)
        self.report_box.configure(state="disabled")

    def export_to_pdf(self):
        # Ensure directory exists
        folder_name = "Weekly_History"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        date_str = datetime.date.today().strftime("%B %d, %Y")
        pdf.cell(200, 10, txt=f"Daily Dozen Prep Guide: {date_str}", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="1. SHOPPING LIST", ln=True)
        pdf.set_font("Arial", '', 10)
        for cat, var in self.selected_items.items():
            item = var.get()
            if item:
                needed = DAILY_DOZEN_TARGETS.get(cat, 1) * SERVING_SIZES.get(cat, 100) * 7
                qty = needed / CONVERSION_FACTORS.get(item, 1.0)
                unit = "g" if qty < 1000 else "kg"
                val = qty if qty < 1000 else qty / 1000
                pdf.cell(200, 8, txt=f"[ ] {item}: {round(val, 2)}{unit}", ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="2. NUTRITIONAL AUDIT", ln=True)
        pdf.set_font("Arial", '', 10)
        
        # Sanitizing for PDF (replacing Unicode emojis/symbols)
        audit_content = self.report_box.get("1.0", "end")
        audit_content = audit_content.replace('☐', '[ ]').replace('⭐', '*').replace('✅', '+').replace('⚠️', '!')
        
        pdf.multi_cell(0, 8, txt=audit_content)

        filename = f"MealPrepPlan_{datetime.date.today()}.pdf"
        full_path = os.path.join(folder_name, filename)
        
        try:
            pdf.output(full_path)
            self.report_box.configure(state="normal")
            self.report_box.insert("1.0", f"\n>>> SUCCESS: Saved to {full_path} <<<\n")
            self.report_box.configure(state="disabled")
        except Exception as e:
            print(f"PDF Error: {e}")
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime

class IPLookupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Lookup Tool - By 4755262")
        self.root.geometry("900x750")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        header_frame = tk.Frame(root, bg="#0a0a0a")
        header_frame.pack(pady=20, fill=tk.X)
        
        title = tk.Label(header_frame, text="⟨ IP LOOKUP TOOL ⟩", 
                        font=("Courier New", 28, "bold"),
                        fg="#00ff00", bg="#0a0a0a")
        title.pack()
        
        signature = tk.Label(header_frame, text="BY 4755262 - DM ONLY BUSINESS",
                           font=("Courier New", 14, "bold"),
                           fg="#ff0000", bg="#0a0a0a")
        signature.pack(pady=5)
        
        separator1 = tk.Frame(root, bg="#00ff00", height=2)
        separator1.pack(fill=tk.X, padx=50, pady=10)
        
        search_frame = tk.Frame(root, bg="#1a1a1a", relief=tk.RIDGE, bd=3)
        search_frame.pack(pady=20, padx=50, fill=tk.X)
        
        search_label = tk.Label(search_frame, text="ADRESSE IP:",
                               font=("Courier New", 12, "bold"),
                               fg="#00ff00", bg="#1a1a1a")
        search_label.pack(side=tk.LEFT, padx=10, pady=15)
        
        self.ip_entry = tk.Entry(search_frame, 
                                font=("Courier New", 12),
                                bg="#0a0a0a", fg="#00ff00",
                                insertbackground="#00ff00",
                                relief=tk.FLAT, bd=2,
                                width=25)
        self.ip_entry.pack(side=tk.LEFT, padx=5, pady=15, ipady=5)
        self.ip_entry.bind('<Return>', lambda e: self.lookup_ip())
        
        self.search_btn = tk.Button(search_frame, text="LOOKUP",
                                    font=("Courier New", 12, "bold"),
                                    bg="#00ff00", fg="#0a0a0a",
                                    activebackground="#00cc00",
                                    relief=tk.FLAT, bd=0,
                                    padx=20, pady=5,
                                    cursor="hand2",
                                    command=self.lookup_ip)
        self.search_btn.pack(side=tk.LEFT, padx=10, pady=15)
        
        self.results_frame = tk.Frame(root, bg="#1a1a1a", relief=tk.RIDGE, bd=3)
        self.results_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        results_title = tk.Label(self.results_frame, text="[ RÉSULTATS ]",
                                font=("Courier New", 14, "bold"),
                                fg="#00ff00", bg="#1a1a1a")
        results_title.pack(pady=10)
        
        canvas = tk.Canvas(self.results_frame, bg="#1a1a1a", 
                          highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", 
                                 command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#1a1a1a")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        self.show_initial_message()
        
        footer = tk.Label(root, text="⟨ IP GEOLOCATION TOOL • POWERED BY 4755262 • 2025 ⟩",
                         font=("Courier New", 9),
                         fg="#666666", bg="#0a0a0a")
        footer.pack(side=tk.BOTTOM, pady=10)
    
    def show_initial_message(self):
        msg = tk.Label(self.scrollable_frame, 
                      text="Entrez une adresse IP pour commencer le scan...",
                      font=("Courier New", 12),
                      fg="#666666", bg="#1a1a1a")
        msg.pack(pady=50)
    
    def clear_results(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def create_info_row(self, label_text, value_text, row_num):
        row_frame = tk.Frame(self.scrollable_frame, bg="#0a0a0a", 
                            relief=tk.RIDGE, bd=1)
        row_frame.pack(fill=tk.X, padx=10, pady=5)
        
        label = tk.Label(row_frame, text=label_text,
                        font=("Courier New", 10, "bold"),
                        fg="#888888", bg="#0a0a0a",
                        anchor="w", width=20)
        label.pack(side=tk.LEFT, padx=10, pady=10)
        
        value = tk.Label(row_frame, text=value_text,
                        font=("Courier New", 11),
                        fg="#00ff00", bg="#0a0a0a",
                        anchor="w", wraplength=500)
        value.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
    
    def get_flag_emoji(self, country_code):
        """Convertit le code pays en emoji drapeau"""
        if not country_code or len(country_code) != 2:
            return "🏳️"
        
        return chr(127397 + ord(country_code[0])) + chr(127397 + ord(country_code[1]))
    
    def lookup_ip(self):
        ip_address = self.ip_entry.get().strip()
        
        if not ip_address:
            messagebox.showwarning("Attention", "Veuillez entrer une adresse IP!")
            return
        
        self.search_btn.config(state=tk.DISABLED, text="SCANNING...")
        self.root.update()
        
        try:
            response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=10)
            data = response.json()
            
            if data.get('error'):
                raise Exception(data.get('reason', 'IP invalide'))
            
            self.clear_results()
            
            flag = self.get_flag_emoji(data.get('country_code', ''))
            country_display = f"{flag}  {data.get('country_name', 'N/A')}"
            
            flag_label = tk.Label(self.scrollable_frame,
                                 text=country_display,
                                 font=("Courier New", 24, "bold"),
                                 fg="#00ff00", bg="#1a1a1a")
            flag_label.pack(pady=20)
            
            separator = tk.Frame(self.scrollable_frame, bg="#00ff00", height=2)
            separator.pack(fill=tk.X, padx=20, pady=10)
            
            info_data = [
                ("IP ADDRESS", data.get('ip', 'N/A')),
                ("TYPE", data.get('version', 'N/A')),
                ("CONTINENT", data.get('continent_code', 'N/A')),
                ("PAYS", data.get('country_name', 'N/A')),
                ("CODE PAYS", data.get('country_code', 'N/A')),
                ("CAPITALE", data.get('country_capital', 'N/A')),
                ("RÉGION", data.get('region', 'N/A')),
                ("CODE RÉGION", data.get('region_code', 'N/A')),
                ("VILLE", data.get('city', 'N/A')),
                ("CODE POSTAL", data.get('postal', 'N/A')),
                ("ADRESSE COMPLÈTE", f"{data.get('city', '')}, {data.get('region', '')}, {data.get('country_name', '')}"),
                ("LATITUDE", str(data.get('latitude', 'N/A'))),
                ("LONGITUDE", str(data.get('longitude', 'N/A'))),
                ("TIMEZONE", data.get('timezone', 'N/A')),
                ("UTC OFFSET", data.get('utc_offset', 'N/A')),
                ("INDICATIF PAYS", data.get('country_calling_code', 'N/A')),
                ("DEVISE", f"{data.get('currency', 'N/A')} ({data.get('currency_name', 'N/A')})"),
                ("LANGUES", data.get('languages', 'N/A')),
                ("ISP/ORGANISATION", data.get('org', 'N/A')),
                ("ASN", data.get('asn', 'N/A')),
                ("DOMAINE ASN", data.get('asn_domain', 'N/A')),
                ("TYPE RÉSEAU", data.get('network', 'N/A')),
                ("TLD", data.get('country_tld', 'N/A')),
                ("POPULATION PAYS", f"{data.get('country_population', 'N/A'):,}" if data.get('country_population') else 'N/A'),
                ("SUPERFICIE (km²)", f"{data.get('country_area', 'N/A'):,}" if data.get('country_area') else 'N/A'),
            ]
            
            for i, (label, value) in enumerate(info_data):
                self.create_info_row(label, str(value), i)
            
            if data.get('latitude') and data.get('longitude'):
                maps_frame = tk.Frame(self.scrollable_frame, bg="#1a1a1a")
                maps_frame.pack(pady=20)
                
                maps_url = f"https://www.google.com/maps?q={data['latitude']},{data['longitude']}"
                maps_label = tk.Label(maps_frame, 
                                     text="🗺️ VOIR SUR GOOGLE MAPS",
                                     font=("Courier New", 11, "bold"),
                                     fg="#00ccff", bg="#1a1a1a",
                                     cursor="hand2")
                maps_label.pack()
                maps_label.bind("<Button-1>", lambda e: self.open_url(maps_url))
                
                coords_label = tk.Label(maps_frame,
                                       text=f"Coordonnées: {data['latitude']}, {data['longitude']}",
                                       font=("Courier New", 9),
                                       fg="#666666", bg="#1a1a1a")
                coords_label.pack()
        
            timestamp = tk.Label(self.scrollable_frame,
                               text=f"Scan effectué le: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                               font=("Courier New", 9),
                               fg="#666666", bg="#1a1a1a")
            timestamp.pack(pady=20)
            
        except requests.exceptions.RequestException as e:
            self.clear_results()
            error_msg = tk.Label(self.scrollable_frame,
                               text=f"⚠ ERREUR RÉSEAU: {str(e)}",
                               font=("Courier New", 12, "bold"),
                               fg="#ff0000", bg="#1a1a1a")
            error_msg.pack(pady=50)
            
        except Exception as e:
            self.clear_results()
            error_msg = tk.Label(self.scrollable_frame,
                               text=f"⚠ ERREUR: {str(e)}",
                               font=("Courier New", 12, "bold"),
                               fg="#ff0000", bg="#1a1a1a")
            error_msg.pack(pady=50)
            
        finally:
            self.search_btn.config(state=tk.NORMAL, text="LOOKUP")
    
    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = IPLookupApp(root)

    root.mainloop()


import sys
import os
import customtkinter
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Logic'))
from networkScan import wifi_available
from networkScan import doh_integrity_check
from riskAnlysis import riskAnalysis

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Public Defender")
        self.geometry("480x520")
        self.resizable(False, False)

        self.tab_view = customtkinter.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_view.add("Network Info")
        self.tab_view.add("Risk Analysis")
        self.tab_view.add("Recommendations")

        self.scan_results = None

        self._build_network_tab()
        self._build_risk_tab()
        self._build_recommendations_tab()

    def _build_network_tab(self):
        tab = self.tab_view.tab("Network Info")

        self.scan_btn = customtkinter.CTkButton(tab, text="Scan Network", command=self._run_scan)
        self.scan_btn.pack(pady=(15, 10))

        self.status_label = customtkinter.CTkLabel(tab, text="", text_color="gray")
        self.status_label.pack()

        info_frame = customtkinter.CTkFrame(tab)
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.fields = {}
        rows = [
            ("SSID",           "ssid"),
            ("Authentication", "auth"),
            ("Cipher",         "cipher"),
            ("IPv4 Address",   "ip"),
            ("Subnet Mask",    "subnet"),
            ("DoH",            "doh"),
            ('DoH Integrity Check', 'doh_check'),
        ]

        for i, (label, key) in enumerate(rows):
            customtkinter.CTkLabel(info_frame, text=f"{label}:", anchor="w", width=140).grid(
                row=i, column=0, padx=(12, 4), pady=6, sticky="w"
            )
            val = customtkinter.CTkLabel(info_frame, text="—", anchor="w")
            val.grid(row=i, column=1, padx=(4, 12), pady=6, sticky="w")
            self.fields[key] = val

    def _build_risk_tab(self):
        tab = self.tab_view.tab("Risk Analysis")
        customtkinter.CTkLabel(tab, text="Run a scan to see risk analysis.", text_color="gray").pack(pady=20)

    def _populate_risk_tab(self):
        if self.scan_results is None:
            return

        tab = self.tab_view.tab("Risk Analysis")

        for widget in tab.winfo_children():
            widget.destroy()

        auth = self.scan_results['auth'] or ''

        auth_risks = {
            'Open':           ('No authentication — traffic is fully exposed to eavesdropping.', 'red'),
            'WPA-Personal':   ('WPA (WPA1) uses TKIP which is deprecated and vulnerable to packet forgery attacks.', 'orange'),
            'WPA-Enterprise': ('WPA (WPA1) Enterprise relies on TKIP which is deprecated and vulnerable to packet forgery attacks.', 'orange'),
            'WPA2-Personal':  ('WPA2-Personal is vulnerable to KRACK (key reuse) and offline dictionary attacks against the PSK due to the 4-way handshake vulnerability.', 'yellow'),
            'WPA2-Enterprise':('WPA2-Enterprise uses 802.1X/RADIUS which is stronger, but still vulnerable to KRACK (key reuse) and the 4-way handshake vulnerability.', 'yellow'),
            'WPA3-Personal':  ('WPA3-Personal uses SAE (replaces PSK) which resists offline dictionary attacks but is still suseptible to the 4-way hanshake capture. Low risk.', 'green'),
            'WPA3-Enterprise':('WPA3-Enterprise with 192-bit mode amd mandatory PMF is the strongest available standard.', 'green'),
        }

        text, color = auth_risks.get(auth, (f'Unrecognized auth method: {auth}', 'gray'))
        customtkinter.CTkLabel(tab, text=f"Auth: {text}", text_color=color, wraplength=400, justify="left").pack(padx=12, pady=(15, 5), anchor="w")

        if self.scan_results['cipher'] and 'TKIP' in self.scan_results['cipher'].upper():
            customtkinter.CTkLabel(tab, text="Cipher: TKIP is deprecated and vulnerable to KRACK-style attacks. CCMP/AES should be used.", text_color="orange", wraplength=400, justify="left").pack(padx=12, pady=5, anchor="w")

        if not self.scan_results['doh']:
            customtkinter.CTkLabel(tab, text="DNS: No DoH detected — DNS queries are unencrypted and visible to network observers including your ISP.", text_color="orange", wraplength=400, justify="left").pack(padx=12, pady=5, anchor="w")

        if self.scan_results['doh_check'] is False:
            customtkinter.CTkLabel(tab, text="DNS Integrity: System DNS response did not match encrypted DoH response — possible DNS spoofing.", text_color="red", wraplength=400, justify="left").pack(padx=12, pady=5, anchor="w")

    def _build_recommendations_tab(self):
        tab = self.tab_view.tab("Recommendations")
        customtkinter.CTkLabel(tab, text="Run a scan to see recommendations.", text_color="gray").pack(pady=20)

    def _populate_recommendations_tab(self):
        if self.scan_results is None:
            return

        tab = self.tab_view.tab("Recommendations")

        for widget in tab.winfo_children():
            widget.destroy()

        auth_risks = ['Open','WPA-Personal','WPA-Enterprise','WPA2-Personal','WPA2-Enterprise']

        if self.scan_results['auth'] in auth_risks:
            customtkinter.CTkLabel(tab, text="Update to a higher Authorization Method: WPA2-Personal is still widely used, but if possible update your router to WPA3", wraplength=400, justify="left").pack(padx=12, pady=5, anchor="w")

        if self.scan_results['cipher'] and 'TKIP' in self.scan_results['cipher'].upper():
            customtkinter.CTkLabel(tab, text="Update to at least WPA2-Personal to use a better cipher", wraplength=400, justify="left").pack(padx=12, pady=5, anchor="w")

        if not self.scan_results['doh']:
            customtkinter.CTkLabel(tab, text="Use a custom dns to encrypt queries. Cloudflare and Google both offer free dns routing (1.1.1.1 and 8.8.8.8)", wraplength=400, justify="left").pack(padx=12, pady=5, anchor="w")

        if self.scan_results['doh_check'] is False:
            customtkinter.CTkLabel(tab, text="Flush your DNS (ipconfig /flushdns in windows) and use a custom dns resolver like Cloudflare or Windows", wraplength=400, justify="left").pack(padx=12, pady=5, anchor="w")

    def _run_scan(self):
        self.scan_btn.configure(state="disabled", text="Scanning...")
        self.status_label.configure(text="")
        self.update()

        #Call backend scan and append the results to the fileds of the tab
        result = wifi_available()

        if result is False:
            self.status_label.configure(text="No Wi-Fi connection detected.", text_color="red")
            self.scan_btn.configure(state="normal", text="Scan Network")
            return

        auth, ssid, cipher, ip, doh, subnet = result

        self.fields["ssid"].configure(text=ssid or "Unknown")
        self.fields["auth"].configure(text=auth or "Unknown")
        self.fields["cipher"].configure(text=cipher or "Unknown")
        self.fields["ip"].configure(text=ip or "Unknown")
        self.fields["subnet"].configure(text=subnet or "Unknown")
        self.fields["doh"].configure(text=doh if doh else "Not detected")

        self.status_label.configure(text="Scan complete.", text_color="green")
        self.scan_btn.configure(state="normal", text="Scan Network")

        #Call the backend DoH query and append the results
        doh_result = doh_integrity_check()

        self.fields["doh_check"].configure(text="Successful" if doh_result else "Failure")

        #Store results for other tabs
        self.scan_results = {
            'auth': auth, 'ssid': ssid, 'cipher': cipher,
            'ip': ip, 'doh': doh, 'subnet': subnet, 'doh_check': doh_result,
        }

        #Update the risk analysis and recommendations tabs
        self._populate_risk_tab()
        self._populate_recommendations_tab()
            
        

app = App()
app.mainloop()

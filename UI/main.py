import sys
import os
import customtkinter
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Logic'))
from networkScan import wifi_available
from networkScan import doh_integrity_check

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
        customtkinter.CTkLabel(tab, text="Risk analysis coming soon.", text_color="gray").pack(pady=20)

    def _build_recommendations_tab(self):
        tab = self.tab_view.tab("Recommendations")
        customtkinter.CTkLabel(tab, text="Recommendations coming soon.", text_color="gray").pack(pady=20)

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

app = App()
app.mainloop()

import SwiftUI

struct SettingsView: View {
    @EnvironmentObject var settings: CompanionSettings

    var body: some View {
        NavigationStack {
            Form {
                Section("Connection") { NavigationLink("Pair read-only Companion") { PairingView() } }
                Section("Interaction") {
                    Toggle("Aegis Voice", isOn: $settings.voiceEnabled)
                    Toggle("ChatGPT Assistant", isOn: $settings.chatGPTEnabled)
                    Text("Visual controls and manual commands remain available when both are off.")
                        .font(.caption)
                }
                Section("Authority") {
                    Picker("Mode", selection: $settings.mode) {
                        Text("RESEARCH").tag("RESEARCH")
                        Text("REPLAY").tag("REPLAY")
                        Text("PAPER").tag("PAPER")
                    }
                    Text("LIVE is intentionally unavailable in this recovered foundation.")
                        .font(.caption)
                }
                Section("Bridge") {
                    TextField("Bridge URL", text: $settings.bridgeURL)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                }
            }
            .navigationTitle("Settings")
        }
    }
}

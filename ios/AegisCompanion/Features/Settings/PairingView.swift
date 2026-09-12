import SwiftUI
struct PairingView: View {
    @EnvironmentObject var settings: CompanionSettings
    @State private var code = ""
    @State private var message = ""
    private let api = CompanionAPI()
    var body: some View { Form { Section("READ-ONLY CONNECTION") { TextField("One-time pairing code", text: $code).keyboardType(.numberPad); Button("Pair device") { Task { await pair() } }; Text(message).foregroundStyle(.secondary) } }.navigationTitle("Pair Companion") }
    private func pair() async { do { let result = try await api.pair(baseURL: settings.bridgeURL, code: code); await MainActor.run { settings.credential = result.credential; message = "Paired with read-only access." } } catch { await MainActor.run { message = "Pairing failed. Check code and connection." } } }
}

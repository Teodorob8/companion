import SwiftUI

struct DiagnosticsView: View {
    let classes = [
        "SAFE_AUTO_FIX", "NEEDS_USER_DECISION", "SECURITY_BLOCKED",
        "DATA_UNAVAILABLE", "DEPENDENCY_MISSING", "CONFIG_INVALID",
        "SERVICE_DOWN", "PERMISSION_DENIED", "UNKNOWN"
    ]

    var body: some View {
        NavigationStack {
            List {
                Section("Recovery") {
                    Label("Safe auto-repair: reversible actions only", systemImage: "wrench.and.screwdriver")
                    Label("Bounded retries + duplicate suppression", systemImage: "arrow.triangle.2.circlepath")
                    Label("Evidence + redaction required", systemImage: "doc.text.magnifyingglass")
                }
                Section("Error classes") {
                    ForEach(classes, id: \.self) { Text($0).font(.caption.monospaced()) }
                }
            }
            .navigationTitle("Diagnostics")
        }
    }
}

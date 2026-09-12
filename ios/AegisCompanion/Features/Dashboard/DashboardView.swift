import SwiftUI

struct DashboardView: View {
    @EnvironmentObject var settings: CompanionSettings

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 12) {
                    statusCard
                    panel("MARKET / OPPORTUNITIES", "Awaiting authenticated Aegis event feed")
                    panel("RISK", "No live authority • mode \(settings.mode)")
                    panel("RESEARCH", "Read-only research projection")
                    panel("SYSTEM HEALTH", "Bridge foundation ready for integration")
                    panel("EVENTS / ALERTS", "No event source connected")
                }
                .padding()
            }
            .navigationTitle("AEGIS COMPANION")
        }
    }

    private var statusCard: some View {
        HStack {
            VStack(alignment: .leading) {
                Text("MISSION STATUS").font(.caption).foregroundStyle(.secondary)
                Text(settings.mode).font(.title2).bold()
                Text("FROZEN SCANNER PROTECTED").font(.caption)
            }
            Spacer()
            Image(systemName: "shield.checkered").font(.largeTitle)
        }
        .padding()
        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 14))
    }

    private func panel(_ title: String, _ detail: String) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title).font(.caption).bold()
            Text(detail).font(.body)
            RoundedRectangle(cornerRadius: 4).frame(height: 2).opacity(0.35)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 14))
    }
}

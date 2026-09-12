import SwiftUI

struct RootView: View {
    var body: some View {
        TabView {
            DashboardView()
                .tabItem { Label("Command", systemImage: "square.grid.2x2") }
            CommandView()
                .tabItem { Label("Search", systemImage: "terminal") }
            DiagnosticsView()
                .tabItem { Label("Health", systemImage: "waveform.path.ecg") }
            SettingsView()
                .tabItem { Label("Settings", systemImage: "gearshape") }
        }
        .preferredColorScheme(.dark)
    }
}

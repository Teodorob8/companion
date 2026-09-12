import SwiftUI

@main
struct AegisCompanionApp: App {
    @StateObject private var settings = CompanionSettings()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(settings)
        }
    }
}

import SwiftUI

@main
struct AegisCompanionApp: App {
    @StateObject private var settings = CompanionSettings()
    @StateObject private var voice = VoiceService()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(settings)
                .environmentObject(voice)
        }
    }
}

import Foundation

final class CompanionSettings: ObservableObject {
    @Published var voiceEnabled = false
    @Published var chatGPTEnabled = false
    @Published var mode = "RESEARCH"
    @Published var bridgeURL = "https://tedslaptop.tailf88ca7.ts.net/companion"
    @Published var credential = ""
}

import AVFoundation
import Foundation

@MainActor
final class VoiceService: ObservableObject {
    private let synthesizer = AVSpeechSynthesizer()
    func speak(_ text: String, enabled: Bool) {
        guard enabled else { return }
        synthesizer.stopSpeaking(at: .immediate)
        let utterance = AVSpeechUtterance(string: text)
        utterance.rate = AVSpeechUtteranceDefaultSpeechRate
        utterance.voice = AVSpeechSynthesisVoice(language: "en-US")
        synthesizer.speak(utterance)
    }
    func stop() { synthesizer.stopSpeaking(at: .immediate) }
}

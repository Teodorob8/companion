import Foundation
struct PairingResponse: Decodable { let credential: String; let scope: String }
enum CompanionAPIError: Error { case failed }
final class CompanionAPI {
    func pair(baseURL: String, code: String) async throws -> PairingResponse {
        var r = URLRequest(url: URL(string: baseURL + "/pairing/redeem")!); r.httpMethod = "POST"
        r.setValue("application/json", forHTTPHeaderField: "Content-Type")
        r.httpBody = try JSONEncoder().encode(["code": code])
        let (d, s) = try await URLSession.shared.data(for: r)
        guard (s as? HTTPURLResponse)?.statusCode == 200 else { throw CompanionAPIError.failed }
        return try JSONDecoder().decode(PairingResponse.self, from: d)
    }
}

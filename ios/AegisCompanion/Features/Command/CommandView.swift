import SwiftUI

struct CommandView: View {
    @State private var command = ""
    @State private var lastResult = "Manual command surface available."

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                TextField("Search or command Aegis…", text: $command)
                    .textFieldStyle(.roundedBorder)
                Button("Submit") {
                    lastResult = command.isEmpty ? "Enter a command." : "Foundation only — command not executed: \(command)"
                    command = ""
                }
                .buttonStyle(.borderedProminent)
                Text(lastResult).frame(maxWidth: .infinity, alignment: .leading)
                Spacer()
            }
            .padding()
            .navigationTitle("Command")
        }
    }
}

import SwiftUI

struct ProfileView: View {
    @State private var notificationsOn = true
    @State private var darkMode = false

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 16) {
                    Image(systemName: "person.circle.fill")
                        .resizable()
                        .frame(width: 80, height: 80)
                        .foregroundColor(.gray)

                    Text("Giulia Rossi")
                        .font(.title2)
                    Text("Member since 2023")
                        .font(.caption)
                        .foregroundColor(.gray)

                    HStack(spacing: 16) {
                        StatCard(title: "Trips", value: "24")
                        StatCard(title: "Countries", value: "7")
                        StatCard(title: "Reviews", value: "12")
                    }

                    VStack(spacing: 0) {
                        Toggle("Notifications", isOn: $notificationsOn).padding()
                        Divider()
                        Toggle("Dark mode", isOn: $darkMode).padding()
                        Divider()
                        Button("Edit profile") {}.padding()
                        Divider()
                        Button("Log out") {}.foregroundColor(.red).padding()
                    }
                    .background(Color.white)
                    .cornerRadius(16)
                    .shadow(color: .black.opacity(0.05), radius: 8)
                }
                .padding()
            }
            .background(Color(.systemGray6))
            .navigationTitle("Profile")
        }
    }
}

struct StatCard: View {
    let title: String
    let value: String

    var body: some View {
        VStack {
            Text(value).font(.title3).bold()
            Text(title).font(.caption).foregroundColor(.gray)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color.white)
        .cornerRadius(16)
        .shadow(color: .black.opacity(0.05), radius: 8)
    }
}

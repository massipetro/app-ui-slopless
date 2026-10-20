import SwiftUI

struct Timetable: Identifiable {
    let id = UUID()
    let title: String
    let year: Int
    let island: String
}

struct LibraryView: View {
    @State private var tab = 0
    private let items = [
        Timetable(title: "Tirrenia Estate", year: 1974, island: "Sardinia"),
        Timetable(title: "Caremar Inverno", year: 1981, island: "Capri"),
        Timetable(title: "SNAV Orari", year: 1992, island: "Ischia"),
    ]

    var body: some View {
        VStack {
            Text("My Timetables")
                .font(.system(size: 34, weight: .bold))
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
            ScrollView {
                VStack(spacing: 16) {
                    ForEach(items) { item in
                        VStack(alignment: .leading, spacing: 8) {
                            Text(item.title).font(.headline)
                            Text("\(item.island) · \(item.year)")
                                .font(.subheadline)
                                .foregroundColor(.gray)
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding()
                        .background(Color.white)
                        .cornerRadius(20)
                        .shadow(color: .black.opacity(0.05), radius: 8, y: 4)
                    }
                }
                .padding()
            }
            Picker("", selection: $tab) {
                Text("Library").tag(0)
                Text("Wishlist").tag(1)
                Text("Settings").tag(2)
            }
            .pickerStyle(.segmented)
            .padding()
        }
        .frame(width: 390, height: 700)
        .background(Color(red: 0.42, green: 0.36, blue: 0.9))
    }
}

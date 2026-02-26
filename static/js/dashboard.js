// JS code to fetch graduates and render table
const tbody = document.querySelector("#graduatesTable tbody");
const searchInput = document.getElementById("searchInput");
let graduatesData = [];

function renderTable(data) {
    tbody.innerHTML = '';
    data.forEach(g => {
        const row = `
        <tr class="hover:bg-gray-50">
            <td class="py-2 px-4 border-b">${g.graduate_id}</td>
            <td class="py-2 px-4 border-b">${g.name}</td>
            <td class="py-2 px-4 border-b">${g.institution_short}</td>
            <td class="py-2 px-4 border-b">${g.course_short}</td>
            <td class="py-2 px-4 border-b">${g.graduation_date}</td>
            <td class="py-2 px-4 border-b">
                <button onclick="printCertificate('${g.graduate_id}')"
                        class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-green-800 transition">
                        Print Certificate
                </button>
            </td>
        </tr>
        `;
        tbody.innerHTML += row;
    });
}

// Fetch graduates once
fetch('/api/graduates')
  .then(res => res.json())
  .then(data => {
      graduatesData = data;
      renderTable(graduatesData);
  });

// Filter as you type
searchInput.addEventListener("input", () => {
    const filter = searchInput.value.toLowerCase();
    const filtered = graduatesData.filter(g =>
        g.graduate_id.toLowerCase().includes(filter) ||
        g.name.toLowerCase().includes(filter) ||
        g.institution_short.toLowerCase().includes(filter) ||
        g.course_short.toLowerCase().includes(filter) ||
        g.graduation_date.toLowerCase().includes(filter)
    );
    renderTable(filtered);
});

function printCertificate(uniqueNumber) {
    alert("Printing certificate for: " + uniqueNumber);
    // Implement PDF or printing functionality here
}
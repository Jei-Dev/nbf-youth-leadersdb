// ========================
// DASHBOARD.JS
// ========================

// DOM elements
const graduatesTableBody = document.querySelector("#graduatesTable tbody");
const searchInput = document.getElementById("searchInput");

// Fetch graduates from API
async function loadGraduates() {
  try {
    const res = await fetch("/api/graduates");
    if (!res.ok) throw new Error("Failed to fetch graduates");
    const grads = await res.json();

    // Clear existing table
    graduatesTableBody.innerHTML = "";

    grads.forEach((grad) => {
      const tr = document.createElement("tr");
      tr.className = "hover:bg-gray-50";

      tr.innerHTML = `
        <td class="py-2 px-4 border-b text-center">${grad.graduate_id}</td>
        <td class="py-2 px-4 border-b text-center">${grad.name}</td>
        <td class="py-2 px-4 border-b text-center">${grad.institution_short}</td>
        <td class="py-2 px-4 border-b text-center">${grad.course_short}</td>
        <td class="py-2 px-4 border-b text-center">${grad.graduation_date}</td>
        <td class="py-2 px-4 border-b text-center">
          <button 
            class="bg-[#2054a8] text-white px-3 py-1 rounded hover:bg-blue-700 transition"
            onclick="printCertificate('${grad.graduate_id}')"
          >
            Print Certificate
          </button>
        </td>
      `;
      graduatesTableBody.appendChild(tr);
    });
  } catch (err) {
    console.error("Error loading graduates:", err);
  }
}

// Filter table as you type
function searchTable() {
  const filter = searchInput.value.toLowerCase();
  const rows = graduatesTableBody.getElementsByTagName("tr");
  for (let i = 0; i < rows.length; i++) {
    const txt = rows[i].textContent.toLowerCase();
    rows[i].style.display = txt.includes(filter) ? "" : "none";
  }
}

// Event listener for search input
if (searchInput) {
  searchInput.addEventListener("keyup", searchTable);
}

// Initialize table
loadGraduates();
document.addEventListener("DOMContentLoaded", () => {

  const dynamicSection = document.getElementById("dynamicSection");
  const chartsSection = document.getElementById("chartsSection");
  const sectionTitle = document.getElementById("sectionTitle");
  const tableHead = document.getElementById("tableHead");
  const tableBody = document.getElementById("tableBody");
  const searchInput = document.getElementById("searchInput");

  const settingsBtn = document.getElementById("settingsBtn");
  const dropdownMenu = document.getElementById("dropdownMenu");

  // -------------------- DROPDOWN --------------------
  settingsBtn.addEventListener("click", () => {
    dropdownMenu.classList.toggle("hidden");
  });

  document.addEventListener("click", (e) => {
    if (!settingsBtn.contains(e.target)) dropdownMenu.classList.add("hidden");
  });

  // -------------------- SHOW/HIDE SECTION --------------------
  function showTableSection(title) {
    chartsSection.classList.add("hidden");
    dynamicSection.classList.remove("hidden");
    sectionTitle.innerText = title;
    tableHead.innerHTML = "";
    tableBody.innerHTML = "";
  }

  window.closeSection = () => {
    dynamicSection.classList.add("hidden");
    chartsSection.classList.remove("hidden");
    tableHead.innerHTML = "";
    tableBody.innerHTML = "";
    searchInput.value = "";
  };

  // -------------------- SEARCH --------------------
  searchInput.addEventListener("keyup", () => {
    const filter = searchInput.value.toLowerCase();
    const rows = tableBody.getElementsByTagName("tr");
    for (let row of rows) {
      row.style.display = row.textContent.toLowerCase().includes(filter) ? "" : "none";
    }
  });

  // -------------------- LOAD GRADUATES --------------------
  window.loadGraduates = () => {
    showTableSection("Graduates");

    tableHead.innerHTML = `
      <tr class="border-b">
        <th class="p-2">Graduate ID</th>
        <th class="p-2">Name</th>
        <th class="p-2">Graduation Date</th>
      </tr>
    `;

    fetch("/api/graduates")
      .then(res => res.json())
      .then(data => {
        tableBody.innerHTML = "";
        data.forEach(r => {
          tableBody.innerHTML += `
            <tr class="border-b">
              <td class="p-2">${r.graduate_id}</td>
              <td class="p-2">${r.name}</td>
              <td class="p-2">${r.graduation_date}</td>
            </tr>
          `;
        });
      });
  };

  // -------------------- LOAD ENROLLMENTS --------------------
  window.loadEnrollments = () => {
    showTableSection("Enrollments");

    tableHead.innerHTML = `
      <tr class="border-b">
        <th class="p-2">Enrollment ID</th>
        <th class="p-2">Name</th>
        <th class="p-2">Institution</th>
        <th class="p-2">Course</th>
        <th class="p-2">Status</th>
      </tr>
    `;

    fetch("/api/enrollments")
      .then(res => res.json())
      .then(data => {
        tableBody.innerHTML = "";
        data.forEach(r => {
          tableBody.innerHTML += `
            <tr class="border-b">
              <td class="p-2">${r.enrollment_id}</td>
              <td class="p-2">${r.name}</td>
              <td class="p-2">${r.institution_short}</td>
              <td class="p-2">${r.course_short}</td>
              <td class="p-2">${r.status}</td>
            </tr>
          `;
        });
      });
  };

  // -------------------- LOAD USERS --------------------
  window.loadUsers = () => {
    showTableSection("Users");

    tableHead.innerHTML = `
      <tr class="border-b">
        <th class="p-2">Name</th>
        <th class="p-2">Username</th>
        <th class="p-2">Role</th>
      </tr>
    `;

    fetch("/api/users")
      .then(res => res.json())
      .then(data => {
        tableBody.innerHTML = "";
        data.forEach(r => {
          tableBody.innerHTML += `
            <tr class="border-b">
              <td class="p-2">${r.name}</td>
              <td class="p-2">${r.username}</td>
              <td class="p-2">${r.role}</td>
            </tr>
          `;
        });
      });
  };

// -------------------- CHARTS --------------------
let institutionChartInstance = null;
let courseYearChartInstance = null;

function loadInstitutionChart() {
  // Fetch combined data for enrollments vs graduates per institution
  Promise.all([
    fetch("/api/chart/institution").then(res => res.json()), // graduates
    fetch("/api/chart/enrollments_per_institution").then(res => res.json()) // enrollments
  ])
  .then(([graduatesData, enrollmentsData]) => {
    const ctx = document.getElementById("institutionChart").getContext("2d");
    if (institutionChartInstance) institutionChartInstance.destroy();

    // Align labels (institution names)
    const labels = Array.from(new Set([...graduatesData.labels, ...enrollmentsData.labels]));

    // Map values to the same label order
    const graduateValues = labels.map(label => graduatesData.labels.includes(label)
      ? graduatesData.values[graduatesData.labels.indexOf(label)] : 0);
    const enrollmentValues = labels.map(label => enrollmentsData.labels.includes(label)
      ? enrollmentsData.values[enrollmentsData.labels.indexOf(label)] : 0);

    institutionChartInstance = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Enrollments",
            data: enrollmentValues,
            backgroundColor: "#2054a8"
          },
          {
            label: "Graduates",
            data: graduateValues,
            backgroundColor: "#1b7a74"
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "top" },
          tooltip: { mode: "index", intersect: false }
        },
        scales: {
          x: { stacked: false },
          y: { beginAtZero: true }
        }
      }
    });
  })
  .catch(error => console.error("Institution Comparison Chart Error:", error));
}

function loadCourseYearChart() {
  fetch("/api/chart/course_year")
    .then(res => res.json())
    .then(data => {
      const ctx = document.getElementById("courseYearChart").getContext("2d");
      if (courseYearChartInstance) courseYearChartInstance.destroy();

      let courses = {};
      let yearsSet = new Set();

      data.forEach(row => {
        const course = row[0];
        const year = parseInt(row[1]);   // <-- convert year to number
        const count = parseInt(row[2]);  // <-- ensure count is number
        yearsSet.add(year);

        if (!courses[course]) courses[course] = {};
        courses[course][year] = count;
      });

      const years = Array.from(yearsSet).sort((a, b) => a - b); // numerical sort
      const datasets = Object.keys(courses).map(course => ({
        label: course,
        data: years.map(y => courses[course][y] || 0),
        fill: false,
        tension: 0.3
      }));

      courseYearChartInstance = new Chart(ctx, {
        type: "line",
        data: { labels: years, datasets },
        options: {
          responsive: true,
          plugins: { legend: { position: "top" } },
          scales: { y: { beginAtZero: true } }
        }
      });
    })
    .catch(error => console.error("Course-Year Chart Error:", error));
}

// Load charts on page load
loadInstitutionChart();
loadCourseYearChart();

});
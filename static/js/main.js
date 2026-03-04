// ----------------------- SEARCH FUNCTION -----------------------
document.getElementById("searchInput").addEventListener("keyup", function() {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll("#enrollmentTable tbody tr");
    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(filter) ? "" : "none";
    });
});

// ----------------------- ENROLLMENT ACTIONS -----------------------
function confirmDelete(id) {
    if (confirm("Are you sure you want to delete this record?")) {
        const deleteForm = document.getElementById("deleteForm") || document.createElement("form");
        deleteForm.method = "POST";
        deleteForm.id = "deleteForm";
        deleteForm.style.display = "none";
        deleteForm.innerHTML = `<input type="hidden" name="delete_id" value="${id}">`;
        document.body.appendChild(deleteForm);
        deleteForm.submit();
    }
}

// ----------------------- EDIT MODAL -----------------------
function openEdit(enrollId, enrollDate, personId, institutionId, courseId) {
    const editBox = document.getElementById("editBox");
    document.getElementById("edit_id").value = enrollId;
    document.getElementById("edit_date").value = enrollDate;
    document.getElementById("edit_person").value = personId;
    document.getElementById("edit_institution").value = institutionId;
    document.getElementById("edit_course").value = courseId;
    editBox.style.display = "flex";
}

function closeEdit() {
    const editBox = document.getElementById("editBox");
    if (editBox) editBox.style.display = "none";
}

// ----------------------- GRADUATE -----------------------
function completeGraduate(enrollId) {
    const today = new Date().toISOString().slice(0, 10);
    const gradDate = prompt("Enter graduation date (YYYY-MM-DD)", today);
    if (!gradDate) return;

    const form = document.createElement("form");
    form.method = "POST";
    form.action = "/add_graduate";

    form.innerHTML = `
        <input type="hidden" name="enrollment_id" value="${enrollId}">
        <input type="hidden" name="graduation_date" value="${gradDate}">
    `;

    document.body.appendChild(form);
    form.submit();
}

// ----------------------- SIDEBAR TOGGLE -----------------------
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebarOverlay");

    if (window.innerWidth < 768) {
        sidebar.classList.toggle("-translate-x-full");
        overlay.classList.toggle("hidden");
    } else {
        sidebar.classList.toggle("w-30");
        sidebar.classList.toggle("w-10");
    }
}

// ----------------------- USER DELETE -----------------------
function confirmUserDelete(userId) {
    if (confirm("Are you sure you want to delete this user?")) {
        fetch(`/delete_user/${userId}`, { method: 'POST' })
        .then(response => response.ok ? location.reload() : alert("Failed to delete user."));
    }
}

// ----------------------- INSTITUTION & COURSE MODALS -----------------------
function openInst() {
    const modal = document.getElementById("instModal");
    if (modal) modal.classList.remove("hidden");
}

function closeInst() {
    const modal = document.getElementById("instModal");
    if (modal) modal.classList.add("hidden");
}

function openCourse() {
    const modal = document.getElementById("courseModal");
    if (modal) modal.classList.remove("hidden");
}

function closeCourse() {
    const modal = document.getElementById("courseModal");
    if (modal) modal.classList.add("hidden");
}

// Optional: close modal when clicking outside content
document.addEventListener("click", function(e) {
    const instModal = document.getElementById("instModal");
    if(instModal && !instModal.querySelector("div").contains(e.target) && !e.target.matches("button")) {
        instModal.classList.add("hidden");
    }
    const courseModal = document.getElementById("courseModal");
    if(courseModal && !courseModal.querySelector("div").contains(e.target) && !e.target.matches("button")) {
        courseModal.classList.add("hidden");
    }
});
// ----------------------- SEARCH FUNCTION -----------------------
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {
        const txt = rows[i].textContent.toLowerCase();
        rows[i].style.display = txt.includes(filter) ? "" : "none";
    }
}

// Usage:
// searchTable('searchInput', 'graduatesTable')
// searchTable('searchInput', 'enrollmentTable')

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

function openEdit(id, date) {
    const editBox = document.getElementById("editBox");
    if (!editBox) return;
    document.getElementById("edit_id").value = id;
    document.getElementById("edit_date").value = date;
    editBox.style.display = "block";
}

function closeEdit() {
    const editBox = document.getElementById("editBox");
    if (editBox) editBox.style.display = "none";
}

function completeGraduate(enrollId) {

    // Default to today's date
    const today = new Date().toISOString().slice(0, 10);

    const gradDate = prompt(
        "Enter graduation date (YYYY-MM-DD)",
        today
    );

    // If user cancels or leaves empty, stop
    if (!gradDate) {
        return;
    }

    // Set hidden form values
    document.getElementById("grad_enroll_id").value = enrollId;
    document.getElementById("grad_date").value = gradDate;

    // Submit form to backend
    document.getElementById("graduateForm").submit();
}

// ----------------------- LOGIN RESET MODAL -----------------------
function openReset() {
    const modal = document.getElementById("resetModal");
    if (modal) modal.classList.remove("hidden");
}

function closeReset() {
    const modal = document.getElementById("resetModal");
    if (modal) modal.classList.add("hidden");
}

// ----------------------- MANAGE USERS MODAL -----------------------
function openUserModal() {
    const modal = document.getElementById("userModal");
    if (modal) modal.style.display = "block";
}

function closeUserModal() {
    const modal = document.getElementById("userModal");
    if (modal) modal.style.display = "none";
}

// ----------------------- SETTINGS MODALS -----------------------
function openInst() {
    const modal = document.getElementById("instModal");
    if (modal) modal.style.display = "block";
}

function closeInst() {
    const modal = document.getElementById("instModal");
    if (modal) modal.style.display = "none";
}

function openCourse() {
    const modal = document.getElementById("courseModal");
    if (modal) modal.style.display = "block";
}

function closeCourse() {
    const modal = document.getElementById("courseModal");
    if (modal) modal.style.display = "none";
}

// ----------------------- DASHBOARD SEARCH -----------------------
document.addEventListener("DOMContentLoaded", () => {
    const searchGraduates = document.getElementById("searchInput");
    if (searchGraduates) {
        searchGraduates.addEventListener("keyup", () => {
            searchTable("searchInput", "graduatesTable");
        });
    }

    const searchEnrollments = document.getElementById("searchInput");
    if (searchEnrollments) {
        searchEnrollments.addEventListener("keyup", () => {
            searchTable("searchInput", "enrollmentTable");
        });
    }
});
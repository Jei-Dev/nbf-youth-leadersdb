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
    const searchInputs = document.querySelectorAll("#searchInput");
    searchInputs.forEach(input => {
        input.addEventListener("keyup", () => {
            const tableId = input.dataset.table;
            searchTable(input.id, tableId);
        });
    });
});

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

function confirmUserDelete(userId) {
    if (confirm("Are you sure you want to delete this user?")) {
        fetch(`/delete_user/${userId}`, {
            method: 'POST',
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("Failed to delete user.");
            }
        });
    }
}
document.addEventListener("DOMContentLoaded", () => {

  loadGraduates();

  document
    .getElementById("searchInput")
    .addEventListener("keyup", filterTable);

});


async function loadGraduates(){

  try{

    const res = await fetch("/api/graduates");
    const data = await res.json();

    const table = document.querySelector("#graduatesTable tbody");
    table.innerHTML="";

    data.forEach(g => {

      const row = document.createElement("tr");

      row.innerHTML = `
      <td class="border px-3 py-2 text-center">${g.graduate_id}</td>
      <td class="border px-3 py-2">${g.name}</td>
      <td class="border px-3 py-2">${g.course_short}</td>
      <td class="border px-3 py-2">${g.institution_short}</td>

      <td class="border px-3 py-2 text-center">
        <span class="bg-green-100 text-green-700 px-2 py-1 rounded text-xs">
          Graduated
        </span>
      </td>

      <td class="border px-3 py-2 text-center space-x-2">

        <button onclick="printGraduate('${g.graduate_id}')"
        class="bg-blue-500 text-white px-2 py-1 rounded text-xs">
          Print
        </button>

        <button onclick="deleteGraduate('${g.graduate_id}')"
        class="bg-red-500 text-white px-2 py-1 rounded text-xs">
          Delete
        </button>

      </td>
      `;

      table.appendChild(row);

    });

    updateCards(data);

  }catch(err){

    console.error("Error loading graduates",err);

  }

}


function filterTable(){

  const input = document
    .getElementById("searchInput")
    .value.toLowerCase();

  const rows = document
    .querySelectorAll("#graduatesTable tbody tr");

  rows.forEach(row => {

    const text = row.innerText.toLowerCase();

    row.style.display =
      text.includes(input) ? "" : "none";

  });

}


function printGraduate(id){

  window.open(`/print_graduate/${id}`, "_blank");

}


async function deleteGraduate(id){

  if(!confirm("Delete this graduate?")) return;

  await fetch(`/delete_graduate/${id}`,{
    method:"DELETE"
  });

  loadGraduates();

}


function updateCards(data){

  let instCount={};
  let courseCount={};

  data.forEach(g=>{

    instCount[g.institution_name]=(instCount[g.institution_name]||0)+1;
    courseCount[g.course_name]=(courseCount[g.course_name]||0)+1;

  });


  function getMax(obj){
    return Object.keys(obj).reduce((a,b)=>obj[a]>obj[b]?a:b);
  }

  function getMin(obj){
    return Object.keys(obj).reduce((a,b)=>obj[a]<obj[b]?a:b);
  }


  document.getElementById("maxInstitution").innerText =
    getMax(instCount);

  document.getElementById("minInstitution").innerText =
    getMin(instCount);

  document.getElementById("maxCourse").innerText =
    getMax(courseCount);

  document.getElementById("minCourse").innerText =
    getMin(courseCount);

}

//Auto populate functions
function calculate_hn24_percent() {
    let hn24= document.getElementById("past_24_hn24").value;
    let swe = document.getElementById("past_24_hn24_swe").value;
    let round_percent = (swe/hn24).toFixed(4) *100;
    document.getElementById("past_24_hn24_percent").value = Number(round_percent);
}
function calculate_ytd_snow(snow) {
    let hn24 = document.getElementById("hn24").value;
    document.getElementById("ytd_snow").value = Number(hn24) + Number(snow);
}

function calculate_ytd_swe(old_swe) {
    let swe = document.getElementById("swe").value;
    let round_percent= (Number(swe) + Number(old_swe)).toFixed(2)
    document.getElementById("ytd_swe").value = Number(round_percent);
}

function togglePwl() {
    let checkbox = document.getElementById("pwl_checkbox");
    let div = document.getElementById("pwl_div");

    if (checkbox.checked) {
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
}
document.addEventListener("DOMContentLoaded", function() {
    togglePwl();
});



//Buttons for update-form avalanches
function addProblem2() {

    document.getElementById("problem_2").hidden = false;
    document.getElementById("problem_2_button").hidden = true;
    document.getElementById("problem_3_button").hidden = false;


}


function addProblem3() {

    document.getElementById("problem_3").hidden = false;
    document.getElementById("problem_3_button").hidden = true;
    document.getElementById("problem_4_button").hidden = false;


}

function addProblem4() {

    document.getElementById("problem_4").hidden = false;
    document.getElementById("problem_4_button").hidden = true;


}


function recheck() {
    alert("this date exists please input a valid date or go to the the view tab to update an existing form.")
    window.location.href = "/view";
}

function confirm_data_delete_am(date){
    if (confirm("Are you sure you want to delete the AM and PM Form for "+date+" ?")) {
        window.location.href = "/view_am/" + date;
    }
}

function confirm_data_delete_pm(date){
    if (confirm("Are you sure you want to delete the PM Form for "+date+" ?")) {
        window.location.href = "/view_pm/" + date;
    }
}



function update_pm_form(pm_form_dates,date) {
        if (pm_form_dates.includes(date)) {
            window.location.href = "/update-pm-form/" + date;
        } else {
            alert("No PM form exists for " + date);
        }
}


let problemCount = 1; // Initial problem count
const maxProblems = 4; // Maximum number of avalanche problems

        function addAvalancheProblem() {
            if (problemCount >= maxProblems) {
                alert("You can only add up to " + maxProblems + " avalanche problems.");
                return;
            }

            problemCount++;
            let newProblem = document.getElementById("problem_1").cloneNode(true);

            // Update IDs and names to be unique
            newProblem.id = "problem_" + problemCount;
            newProblem.querySelectorAll("select, input").forEach(element => {
                let name = element.name.replace(/\d+/, problemCount); // Update number in names
                element.name = name;
                element.id = name;
                if (element.type === "checkbox"){
                    element.checked = false;
                }
                else if (element.type === "text"){
                    element.value="";
                }

            });

            // Update heading
            newProblem.querySelector("h3")?.remove();
            let heading = document.createElement("h3");
            heading.textContent = "Avalanche Problem " + problemCount;
            newProblem.prepend(heading);

            // Add a remove button (only for additional problems)
            let removeBtn = document.createElement("button");
            removeBtn.type = "button";
            removeBtn.textContent = "Remove";
            removeBtn.onclick = function () { removeAvalancheProblem(newProblem.id); };
            newProblem.appendChild(removeBtn);

            document.getElementById("problems-container").appendChild(newProblem);
            if (document.getElementById('problem_2')) {
                document.getElementById('remove_1').hidden = true;
            }
            else{
                document.getElementById('remove_1').hidden = false;
            }
        }

        function removeAvalancheProblem(id) {
            document.getElementById(id).remove();
            problemCount--;
            if (document.getElementById('problem_2')) {
                document.getElementById('remove_1').hidden = true;
            }
            else{
                document.getElementById('remove_1').hidden = false;
            }
        }
function removeAvalancheProblem1(id) {

    document.getElementById(id).hidden = true;
    document.getElementById('restore').hidden = false;
    document.getElementById('add_avy').hidden = true;
    document.getElementById('remove_1').hidden = true;
    resetProblem1Fields();
}
function resetProblem1Fields() {
    // Reset dropdowns
    document.getElementById("location1").value = "";
    document.getElementById("avalanche_problem_1").value = "";

    // Reset checkboxes (all aspects at all elevations)
    const checkboxNames = [
        "btl_aspect_1[]", "ntl_aspect_1[]", "atl_aspect_1[]"
    ];
    checkboxNames.forEach(name => {
        const checkboxes = document.getElementsByName(name);
        checkboxes.forEach(cb => cb.checked = false);
    });

    // Reset text inputs
    document.getElementById("size_1").value = "";
    document.getElementById("likelihood_1").value = "";
}

function restoreProblem1() {
    let problem1 = document.getElementById("problem_1");
    if (problem1) {
        problem1.hidden = false;
    }
    document.getElementById('restore').hidden = true;
    document.getElementById('add_avy').hidden = false;
     document.getElementById('remove_1').hidden = false;
}
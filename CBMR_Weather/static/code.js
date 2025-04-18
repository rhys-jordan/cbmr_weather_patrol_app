
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
    if (confirm("Are you sure you want to delete the AM Form for "+date+" ?")) {
        window.location.href = "/view_am/" + date;
    }
}

function confirm_data_delete_pm(date){
    if (confirm("Are you sure you want to delete the PM Form for "+date+" ?")) {
        window.location.href = "/view_pm/" + date;
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
        }

        function removeAvalancheProblem(id) {
            if (problemCount > 1) {
                document.getElementById(id).remove();
                problemCount--;
            } else {
                alert("At least one avalanche problem must be present.");
            }
        }


function adjust () {

    var slider = document.getElementById('slider');
    var output = document.getElementById('link');
    var link = "/isPrime/";

    slider.oninput = function() {
        output.innerHTML = this.value;
        output.href = link.concat(this.value); 

    } 

}





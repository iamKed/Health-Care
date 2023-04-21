
// let signup = document.querySelector(".signup");
// let login = document.querySelector(".login");
// let slider = document.querySelector(".slider");
// let formSection = document.querySelector(".form-section");

// signup.addEventListener("click", () => {
//     slider.classList.add("moveslider");
//     formSection.classList.add("form-section-move");
// });

// login.addEventListener("click", () => {
//     slider.classList.remove("moveslider");
//     formSection.classList.remove("form-section-move");
// });


// // change the border while entering the values

// // let iptag=document.querySelector(".ele");

// function A() {
//     slider.classList.remove("moveslider");
//     formSection.classList.remove("form-section-move");
// }
// function B() {
//     slider.classList.add("moveslider");
//     formSection.classList.add("form-section-move");
// }
// function CBorder(tag) {

// }


// password eye icon to show and hide icon
const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#id_password');

// togglePassword.addEventListener('click', function (e) {
//     // toggle the type attribute
//     const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
//     password.setAttribute('type', type);
//     // toggle the eye slash icon
//     togglePassword.classList.toggle('fa-eye-slash');
// });

// const togglePassword1 = document.querySelector('#togglePassword1');
// const password1 = document.querySelector('#id_password1');

// togglePassword1.addEventListener('click', function (e) {
//     // toggle the type attribute
//     // window.alert("Toggle happend");
//     const type1 = password1.getAttribute('type') === 'password' ? 'text' : 'password';
//     password1.setAttribute('type', type1);
//     // toggle the eye slash icon
//     togglePassword1.classList.toggle('fa-eye-slash');
// });

// const togglePassword2 = document.querySelector('#togglePassword2');
// const password2 = document.querySelector('#id_password2');

// togglePassword2.addEventListener('click', function (e) {
//     // toggle the type attribute
//     const type2 = password2.getAttribute('type') === 'password' ? 'text' : 'password';
//     password2.setAttribute('type', type2);
//     // window.alert("function called.....");
//     // toggle the eye slash icon
//     togglePassword2.classList.toggle('fa-eye-slash');
// });


function Show(tag){
    let t=document.querySelector(tag);

    const type = t.getAttribute('type') === 'password' ? 'text' : 'password';
    t.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
}


// +==================== Validation section ==================== 

//  +++++++++ Password Strength checker using jQuery ++++++++++++++

// $(function(){

//   $('input#demo').passwordstrength({
//   'minlength': 6, // Minimum length of password
//   'number'   : true, // Password requires at least one number
//   'capital'  : true, // Password requires at least one uppercase letter
//   'special'  : true, // Password requires at least one special character
//   'labels'   : {
//   'general'   : 'The password must have :',
//   'minlength' : 'At leaset {{minlength}} characters',
//   'number': 'At least one number',
//   'capital'   : 'At least one uppercase letter',
//   'special'   : 'At least one special character'
//   }
//   });

//   });


//  =============================================


let passwordInfo = document.getElementById('passwordInfo');
let passwordInput = document.getElementById("form3Example9_ps");



// define regex for different password stength
let poorReg = /[a-z]/; // password consist of only letters
let weakReg = /(?=.*?[0-9])/;
let strongReg = /(?=.*?[#?!@$%^&*-])/;
let whiteSpaceReg = /^$|\s+/;

// PassValidate()

// passwordInput.onkeyup=function (e) { 
    function PassValidate(){
    console.log("key pressed");
    let passVal = document.getElementById('form3Example9_ps').value;
    let passLen = passVal.length;
    console.log(passVal);

    let poorPassword = passVal.match(poorReg);
    let weakPassword = passVal.match(weakReg);
    let strongPassword = passVal.match(strongReg);
    let whiteSpace = passVal.match(whiteSpaceReg);


    if (passVal != "") {
        if (whiteSpace) {
            document.getElementById('passwordInfo').textContent = "White spaces are not allowed";
        }
        else {
            poorPasswordStrength(passLen, poorPassword, weakPassword, strongPassword);
            weakPasswordStrength(passLen, poorPassword, weakPassword, strongPassword);
            strongPasswordStrength(passLen, poorPassword, weakPassword, strongPassword);
            // passwordInfo.textContent="Use character, digits and symbol";
            // passwordInfo.textContent="";
        }
    } else {
        // passwordInfo.style.display='none';
        document.getElementById('passwordInfo').textContent = "";
    }

}

function poorPasswordStrength(passLen, poorPassword, weakPassword, strongPassword) {

    if (passLen <= 3 && (poorPassword || weakPassword || strongPassword)) {
        // passwordInfo.style.display="block";
        document.getElementById('passwordInfo').style.color = 'red';
        document.getElementById('passwordInfo').textContent = "your password is too poor";
        console.log("Poor Password function get called");
    }
}

function weakPasswordStrength(passLen, poorPassword, weakPassword, strongPassword) {
    //   console.log("Weak Password function get called");
    if (passLen >= 6 && poorPassword && (weakPassword || strongPassword)) {
        // passwordInfo.style.display="block";
        document.getElementById('passwordInfo').style.color = 'orange';
        document.getElementById('passwordInfo').textContent = "Password Strength: Weak";

    } else {
        document.getElementById('passwordInfo').textContent = "Use Special symbol and length will be atleast 8";
    }
}

function strongPasswordStrength(passLen, poorPassword, weakPassword, strongPassword) {
    //   console.log("Strong Password function get called");
    if (passLen >= 8 && (poorPassword && weakPassword) && strongPassword) {

        // passwordInfo.style.display="block";
        document.getElementById('passwordInfo').style.color = 'green';
        document.getElementById('passwordInfo').textContent = "Password Strength: Strong";

    } else {
        // passwordInfo.textContent="Use";
        // passwordInfo.style.display='none';

    }
}

// +++++++++++++++++++ Conform password validation ++++++++++++++++++++++++

// var pw=document.getElementById("pid");
var msg = document.getElementById('msg');
function validation(tag) {
    var cfpw = document.getElementById(tag);
    var pw = document.getElementById("form3Example9_cf");
    // console.log(cfpw.value);
    // console.log(pw.value);
    if (cfpw.value != pw.value) {
        cfpw.style.border = "2px solid rgb(252, 148, 148)";
        // msg.style.display='relative';
        msg.textContent = "Please enter same password";
        // return false;
    }
    else {
        cfpw.style.border = "2px solid rgb(128, 247, 255)";
        console.log("Password is matched....")
        msg.style.display = 'none';
        msg.textContent = '';
        // return true;
    }

}
function checkIt() {
    var cfpw = document.getElementById("form3Example9_ps").value;
    var pw = document.getElementById("form3Example9_cf").value;
    if (cfpw!= pw) {
        console.log("Please enter valid password....")
        window.alert("Please Enter Same Password")
    }
}


// change the border color
function changeB(tag) {
    let t = document.querySelector(tag);
    console.log(t.value);
    console.log("inside the changeB");

    t.style.border = '2px solid rgb(128, 247, 255)';
    t.style.boxShadow = '2px black';

}

function myalert() {
    alert("Wrong Password");
}









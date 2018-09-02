
const loginUser = () => {
    
    fetch('https://mydiary-basweti.herokuapp.com/v1/auth/login', {
        method: 'POST',
        body: JSON.stringify({
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
        }),
        headers: {
            'Accept': 'application/json',
            'Content-type': 'application/json',
            "redirected":false
        }
    })
        .then((response) => response.json())
        .then((json) => {
            console.log(json)
            if (json.message ==="wrong password"){
                document.getElementById('errors').style.color = 'red'
                document.getElementById('errors').innerHTML = 'wrong password'
            }
            else if (json.message ==="user does not exist"){
                document.getElementById('errors').style.color = 'red'
                document.getElementById('errors').innerHTML = 'user does not exist'
                
            }
            else if (json.token){
                console.log(json.token)
                window.location.replace("dashboard.html")
                localStorage.setItem("token",json.token)
                
                
            }else{
                alert('invalid cridentials')
            }
        })
}


const addUser = () => {
    if (document.getElementById('password').value == document.getElementById('confirm').value){

    fetch('https://mydiary-basweti.herokuapp.com/v1/auth/registration', {
        method: 'POST',
        body: JSON.stringify({
            
            name:document.getElementById('name').value,
            username:document.getElementById('username').value,
            password:document.getElementById('password').value,
            email:document.getElementById('email').value
        }),
        headers: {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        }
    })
        .then((response) => response.json())
        .then((json) => {
            console.log(json)
            if (json.message === "Password should be 6 characters and above") {
                document.getElementById('nomatch').style.color = 'red'
                document.getElementById('nomatch').innerHTML = 'password should be 6 characters or more'
                
            }
            
            else if (json.message ==="email is already taken"){
                document.getElementById('nomatch').style.color = 'red'
                document.getElementById('nomatch').innerHTML = 'email already exists'
                
            }
            
            else if (json.message === "email not valid,change format") {
                document.getElementById('nomatch').style.color = 'red'
                document.getElementById('nomatch').innerHTML = 'email is not valid'
                
            }
            else if (json.message === "No fields should be empty") {
                document.getElementById('nomatch').style.color = 'red'
                document.getElementById('nomatch').innerHTML = 'Fill all the fields please'
                
            }
            else if (json.message === "user created") {
                window.location.replace("login.html")
                document.getElementById('nomatch').style.color = 'green'
                document.getElementById('nomatch').innerHTML = 'user created,login with your credentials'
            }

        })
    
    }else{
        document.getElementById('password').style.color='red';
        document.getElementById('nomatch').style.color = 'red';
        document.getElementById('confirm').style.color = 'red'
        document.getElementById('nomatch').innerHTML = 'passwords do not match'
    }

}

function getEntry(){
    var access_token = localStorage.getItem("token")
    if (!access_token){
        window.location.replace('login.html')
    }
    fetch('https://mydiary-basweti.herokuapp.com/v1/entries/', {
        headers: {
            "x-access-token": access_token
        }
    })
        .then(response => response.json())
        .then(data => {
            let output = `<h2>Welcome </h2>`;
            console.log(data);
            
            data.forEach(function (entry) {
                
                output += `
                
                <div class="speech-bubble">
                    <td><h2>${entry.title}</h2></td>
                    <p style="
                        display:-webkit-box;
                        -webkit-line-clamp:2;
                        overflow:hidden;
                        -webkit-box-orient:vertical;
                    ">${entry.body}</p>
                    <button  type="button" value="${entry.id}" onclick="getOneEntry(this.value)" class="btn-detail">More</button>
                    <button  type="button" value="${entry.id}" onclick="updateEntry(this.value)" class="btn-edit">Edit Post</button>              
                    <button  type="button" value="${entry.id}" onclick="DeleteEntry(this.value)" class="btn-delete">Delete</button>
                    <td><a class="btn-share"><img src="./img/share1.png" alt=""></a></td>
                    <td ><small style="position:absolute;right:2;bottom:10;float:right;">Written by ${entry.username}</small></td>
                    
                </div>
                    
                    `
                    ;
            });
            console.log(data);
            document.getElementById('output').innerHTML = output;
        })
}

const addEntry = () => {
    var access_token = localStorage.getItem("token")
    if (!access_token) {
        window.location.replace('login.html')
    }
    fetch('https://mydiary-basweti.herokuapp.com/v1/entries/', {
        method: 'POST',
        body: JSON.stringify({

            body: document.getElementById('body').value,
            title: document.getElementById('title').value,
            
        }),
        headers: {
            'Accept': 'application/json',
            'Content-type': 'application/json',
            "x-access-token": access_token
        }
    })
        .then((response) => response.json())
        .then((json) => {
            console.log(json)
            if (json.message ==="field cannot be empty"){
                document.getElementById('confirm').style.color = 'red'
                document.getElementById('confirm').innerHTML = 'no field can be empty'
            }
            else if (json.result === "entry added") {
                window.location.replace("dashboard.html")
            }

            
        })
}

function getOneEntry(val) {
    var access_token = localStorage.getItem("token")
    console.log(val)
    fetch(`https://mydiary-basweti.herokuapp.com/v1/entries/${val}`,{
        headers: {
            "x-access-token": access_token
            
        }
    })
        .then(response => response.json())
        .then(data => {
            let output = '<td><a href="dashboard.html" class="btn">back</a></td>';
            console.log(data);
              
                output += `
                <div class="col">
                <div class="speech-bubble">
                
                    <td><h2 style="text-align:center;">${data.title}</h2> </td>
                    
                
                    <p>${data.body}</p>
                    
                    <button  type="button" value="${data.id}" onclick="updateEntry(this.value)" class="btn-edit">Edit Post</button> 
                    <button  type="button" value="${data.id}" onclick="DeleteEntry(this.value)" class="btn-delete">Delete</button>
                    <td><a class="btn-share"><img src="./img/share1.png" alt=""></a></td>
                    
                </div>    
                </div>
                    
                    `
                    ;
            
            console.log(data);
            document.getElementById('output').innerHTML = output;
        })
}

function updateEntry(val) {
    var access_token = localStorage.getItem("token")
    console.log(val)
    fetch(`https://mydiary-basweti.herokuapp.com/v1/entries/${val}`, {
        
       
        headers: {
            "x-access-token": access_token

        }
    })
        .then(response => response.json())
        .then(data => {
            let output = '<td><a href="dashboard.html" class="btn">back</a></td>';
            console.log(data);

            output += `
                <div class="col">
                <div id="confirm">

                </div>
               <form >
                            <div>
                                <label for="">Title:</label>
                                <br>
                                <input type="text" name="" value="${data.title}" id="title">
                            </div>
                            <div>
                                <label for="">Story</label>
                                <br>
                                <textarea  id="body" cols="30" rows="10">${data.body}</textarea>
                            </div>
                            <button type="button"value="${data.id}" class="btn" onclick="updateEditEntry(this.value)">Post</button>
                        </form>
                </div>

                <script src="https://cdn.ckeditor.com/4.9.2/standard/ckeditor.js"></script>
<script>
    CKEDITOR.replace('body');
</script>
                    
                    `
            

                ;

            console.log(data);
            document.getElementById('output').innerHTML = output;
        })
        
}

const updateEditEntry = (val) => {
    var access_token = localStorage.getItem("token")
    fetch(`https://mydiary-basweti.herokuapp.com/v1/entries/${val}`, {
        method: 'PUT',
        body: JSON.stringify({

            body: document.getElementById('body').value,
            title: document.getElementById('title').value,

        }),
        headers: {
            'Accept': 'application/json',
            'Content-type': 'application/json',
            "x-access-token": access_token
        }
    })
        .then((response) => response.json())
        .then((json) => {
            console.log(json)
            if (json.message ==="field cannot be empty"){
                document.getElementById('confirm').style.color = 'red'
                document.getElementById('confirm').innerHTML = 'no field can be empty'
            }
            else if (json.message === "entry updated") {
                window.location.replace("dashboard.html")
            }


        })
}

const DeleteEntry = (val) => {
    var access_token = localStorage.getItem("token")
    var del=confirm("Are you sure want to delete?")
    if (del) {

            
            fetch(`https://mydiary-basweti.herokuapp.com/v1/entries/${val}`, {
                method: 'DELETE',
                headers: {
                    'Accept': 'application/json',
                    'Content-type': 'application/json',
                    "x-access-token": access_token
                }
            })
                .then((response) => response.json())
                .then((json) => {
                    console.log(json)
                    if (json.message === "entry deleted") {
                        window.location.replace("dashboard.html")
                        window.alert("Entry Deleted")
                    }


                })
    }
    else{
        return false;
    }
}


function logOut() {
    var access_token = localStorage.getItem("token")
    if(access_token){
        localStorage.removeItem("token")
        window.location.replace("login.html")
    }


}

//user details
function getUser() {
    var access_token = localStorage.getItem("token")
    if (!access_token) {
        window.location.replace('login.html')
    }
    fetch('https://mydiary-basweti.herokuapp.com/v1/auth/user', {
        headers: {
            "x-access-token": access_token
        }
    })
        .then(response => response.json())
        .then(user => {
            let title = `<h2>Hello ${user.name}`;
            
            let userProfile = `
            
            <img src="./img/default-user.png" alt="">
                    <p><i>Your Profile Pic</i></p>
                    <p><b>USERNAME:</b>${user.username} </p>
            `;
            let output = `<h4>Here is Your Profile <i>${user.username}</i></h4>`;

            let entries = `<h2>No of Entries...</h2>
                        <code><h2>${user.entries} <i>entries so far...</i></h2> </code>`
            
            console.log(user);

            

                output += `
                <div class="col">
                        <p><b>FIRST NAME:</b> ${user.name}</p>
                        
                        <p><b>EMAIL:</b> ${user.email}</p>
                        <p><b>USERNAME:</b> ${user.username}</p>
                        <p><b>DATE JOINED:</b>${user.date}</p>
                    </div>
                    
                    `
                    ;
           
            console.log(user);
            document.getElementById('name').innerHTML = title;
            document.getElementById('output').innerHTML = output;
            
            document.getElementById('user').innerHTML = userProfile;
            document.getElementById('entries').innerHTML = entries;
            
        })
}

//delete account
const DeleteAccount = () => {
    var access_token = localStorage.getItem("token")
    var del = confirm("Are you sure want to delete your account?")
    if (del) {


        fetch(`https://mydiary-basweti.herokuapp.com/v1/auth/delete`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-type': 'application/json',
                "x-access-token": access_token
            }
        })
            .then((response) => response.json())
            .then((json) => {
                console.log(json)
                if (json.message === "user deleted") {
                    window.location.replace("registration.html")
                    window.alert("Your account has been Deleted")
                }


            })
    }
    else {
        return false;
    }
}

//retrieve user data for editing
function getEditingInfor() {
    var access_token = localStorage.getItem("token")
    if (!access_token) {
        window.location.replace('login.html')
    }
    fetch('https://mydiary-basweti.herokuapp.com/v1/auth/user', {
        headers: {
            "x-access-token": access_token
        }
    })
        .then(response => response.json())
        .then(user => {
            let output = `<h4>Here is Your Profile <i>${user.username}</i></h4>`;
            console.log(user);
            output += `<div id="nomatch">
                            
                        </div>
                        <form>
                            <div>
                                <label>Name:</label>
                                <br>
                                <input type="text" value="${user.name}" placeholder="Name" id="name1" name="name" required>
                            </div
                            
                            <div>
                                <label>Username:</label>
                                <br>
                                <input type="text" value="${user.username}"   id="username" required>
                            </div>
                            <div>
                                <label>Email:</label>
                                <br>
                                <input type="email"value="${user.email}"  id="email"  required>
                            </div>
                            <div>
                                <label>Password:</label>
                                <br>
                                <input type="password"   id="password" required>
                            </div>
                            <div>
                                <label>Confirm Password:</label>
                                <br>
                                <input type="password" placeholder="Confirm Password" id="confirm"  required>
                            </div>
                            
                            <button type="button" onclick="editUser()" class="btn">submit</button>
                        </form>
                    
                    `
                ;

            console.log(user);
            document.getElementById('output').innerHTML = output;
            
        })

        

}
//edit user

const editUser = () => {
    var access_token = localStorage.getItem("token")
    if (document.getElementById('password').value == document.getElementById('confirm').value) {

        fetch('https://mydiary-basweti.herokuapp.com/v1/auth/user/update/', {
            method: 'PUT',
            body: JSON.stringify({

                name: document.getElementById('name1').value,
                username: document.getElementById('username').value,
                password: document.getElementById('password').value,
                email: document.getElementById('email').value
                
            }),
            headers: {
                'Accept': 'application/json',
                'Content-type': 'application/json',
                "x-access-token": access_token
            }
        })
            .then((response) => response.json())
            .then((json) => {
                console.log(json)
                if (json.message === "Password should be 6 characters and above") {
                    document.getElementById('nomatch').style.color = 'red'
                    document.getElementById('nomatch').innerHTML = 'password should be 6 characters or more'

                }

                else if (json.message === "email is already taken") {
                    document.getElementById('nomatch').style.color = 'red'
                    document.getElementById('nomatch').innerHTML = 'email already exists'

                }

                else if (json.message === "email not valid,change format") {
                    document.getElementById('nomatch').style.color = 'red'
                    document.getElementById('nomatch').innerHTML = 'email is not valid'

                }
                else if (json.message === "No fields should be empty") {
                    document.getElementById('nomatch').style.color = 'red'
                    document.getElementById('nomatch').innerHTML = 'Fill all the fields please'

                }
                else if (json.message === "user updated") {
                    window.location.replace("profile.html")
                    document.getElementById('nomatch').style.color = 'green'
                    document.getElementById('nomatch').innerHTML = 'user created,login with your credentials'
                }

            })

    } else {
        document.getElementById('password').style.color = 'red';
        document.getElementById('nomatch').style.color = 'red';
        document.getElementById('confirm').style.color = 'red'
        document.getElementById('nomatch').innerHTML = 'passwords do not match'
    }

}

//navbar
function login(){
    var access_token = localStorage.getItem("token")
    console.log(window.location.href)
    if (access_token) {
       
        let log=`
            <li>
                <a href="dashboard.html">Dashboard</a>
            </li>
            <li>
                <a href="profile.html">Profile</a>
            </li>
            <li>
                <a href="" onclick="logOut()">Logout</a>
            </li>
        `
        
        document.getElementById('login').innerHTML = log;
        
    } else {
        if (window.location.href === "https://michael-basweti.github.io/UI/index.html") {
            let log = `
            
            <li>
                <a href="login.html">SIGN IN</a>
            </li>
            <li>
                <a href="registration.html">Sign Up</a>
            </li>
        `
            document.getElementById('login').innerHTML = log;
        }
        else if (window.location.href === "https://michael-basweti.github.io/UI/login.html"){
            let log = `
            
            <li>
                <a href="index.html">home</a>
            </li>
            <li>
                <a href="registration.html">Sign Up</a>
            </li>
        `
            document.getElementById('login').innerHTML = log;
        }
        else if (window.location.href === "https://michael-basweti.github.io/UI/registration.html") {
            let log = `
            
            <li>
                <a href="index.html">home</a>
            </li>
            <li>
                <a href="login.html">Sign in</a>
            </li>
        `
            document.getElementById('login').innerHTML = log;
        }
        
        
        
        
    }
    
    
}
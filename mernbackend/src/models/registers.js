const mongoose=require("mongoose");

const employeeSchema=new mongoose.Schema({
    firstname:{
        type: String,
        required:true
    },
    lastname:{
        type: String,
        required:true
    },
    gender:{
        type: String,
        required:true
    },
    mobileno:{
        type: Number,
        required:true,
        unique:true
    },
    
    rollno:{
        type: Number,
        required:true,
        unique:true
    },
    emailid:{
        type: String,
        required:true
        //unique:true
    },
    password:{
        type: String,
        required:true
    },
    confirmpassword:{
        type: String,
        required:true
    }
})

const Register=new mongoose.model("Register",employeeSchema);
module.exports=Register;
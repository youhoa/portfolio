const wrapperBax = document.getElementById("wrapper");
const inputFieldGroup =  document.getElementsByClassName("inputGroup")
const allInputs = document.querySelectorAll("input");
const userNickname = document.getElementById("nickname");
const userEmail = document.getElementById("email");
const userPassword = document.getElementById("userPassword");
const confirmPassword = document.getElementById("confirmPassword");
const userPhone = document.getElementById("phone");
const registrationForm = document.getElementById("registrationForm");

const updateHelperText = (input,message,isValid)=>{
    const inputGroup = input.parentElement;
    //한개의 input태그의 부모 태그에 접근하는 것
    //ex)input태그를 저희가 userEmail로 접근하였다고 하면,
    //아래 태그들의 최상위태그를 의미한다
    const helperText = inputGroup.getElementsByClassName("helperText")[0];
    //알림
    if(isValid==true){
        //isVaild에는 boolean데이터 true/false가 들어가게끔 만든다.
        inputGroup.classList.remove('invalid');
        inputGroup.classList.add('valid');
        helperText.style.visibility = "hidden";
    }
    if(isValid==false){
        inputGroup.classList.remove('valid');
        inputGroup.classList.add('invalid');
        helperText.style.visibility = "visible";
        helperText.innerText = message;
    }

    };

    //알림이 사용이되는것까지는 설정을 했는데 언제 사용이 되야하냐 조건을 설정 안했음
    //입력필드가 비어있는지 확인하는 함수기능을 만든다
    const checkEmptyInput = (input) =>{
        if(input.value.trim()===''){
            //인풋입력칸에 입력한 문자열중 띄어쓰기를 없애는 기능
            updateHelperText(input,'값을 입력해주세요.',false);
            return false;
        }else{
            //입력이 있으면 도움말을 지웁니다
            updateHelperText(input,"",true);
            return true;
        }
    }


    //이메일형식이 올바른지 확인하는 함수
    //이메일 주소가 규칙에 맞게 작성이되었는지 확인하는것
    const validateEmailFormat = (input)=>{
        function updateHelperText() {
    const emailInput = document.getElementById('email');
    const helperText = document.getElementById('email-helper');

    if (emailInput.value == false) {
        helperText.textContent = 'asdf';
        helperText.style.color = 'red';
    }
}
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;
        if(emailPattern.test(input.value.trim())==true){
            updateHelperText(input,"",true);
            return true;
        }else{
            updateHelperText(input,"올바른 이메일 형식이 아닙니다.");
            return false;
        }
        //정규식 => 마법, 이메일에 골뱅이가 들어갔다거나 .com,co.kr이런식으로 표현이 안될때
        //검사를 해가지고 true혹은 false를 리턴하게 할수있다 => 이메일 정규식
    }

//비밀번호 강도 설정
const checkPasswordStrength = (password)=>{
    const strongPattern = /^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{8,15}$/;   
    if(strongPattern.test(password.value)==true){
        updateHelperText(password,"비밀번호 강도:강함",true);
        return true;
    }else{
        updateHelperText(password,"비밀번호는 8자 이상이어야하며, 대문자, 소문자, 특수문자를 포함하여야합니다.");
        return false;
    }
}
//비밀번호와 비밀번호 확인입력칸이 같은지 확인
const validatePasswordMatch = (passwordInput,confirmInput)=>{
    if(passwordInput.value !== confirmInput.value){
        updateHelperText(confirmInput,"비밀번호가 일치하지 않습니다.",false);
        return false;
    }else{
        updateHelperText(confirmInput,"",true);
        return true;
    
    }
}

//전화번호가 올바른 형식인지 확인하는 함수
const validatePhoneNumber = (input)=>{
    const phonePattern = /^\d{3}-\d{3,4}-\d{4}$/;
    if(phonePattern.test(input.value.trim())){
        updateHelperText(input,"",true);
        return true;
    }else{
        updateHelperText(input,"올바른 전화번호 형식이 아닙니다.(예시:010-1234-5678)",false);
        return false;
    
    }
}


//폼제출시(회원가입버튼누르면 회원가입진행되게끔 하는것)입력필드가 유효한지 확인하는 함수
//숙제 검사에서 모든 항목을 검토하는것과 같다
const validateForm = () => {
    const isNicknameValid = checkEmptyInput(userNickname);
    //boolean값으로 에러검사시 문제가 없으면 true를 값으로 가지고 있으면 false를 값으로 가진다
    const isEmailValid = validateEmailFormat(userEmail);
    const isPasswordValid = checkPasswordStrength(userPassword);
    const isPasswordMatch = validatePasswordMatch(userPassword,confirmPassword);
    const isPhoneValid = validatePhoneNumber(userPhone);

    //모든 검사를 해서 모든 검사가 통과해야 회원가입버튼을 눌렀을때 회원가입이 진행되게끔 한다
    return isNicknameValid && isEmailValid && isPasswordValid && isPasswordMatch && isPhoneValid;
    //모든 조건들 isNicknameValid이런 변수들은 전부 현재 boolean데이터를 가지고 있고
    //전부 true여야지 true값을 반환한다.
}

registrationForm.addEventListener("submit",(e)=>{
    //폼안의 submit타입의 버튼을 눌렀을 때 이벤트가 발생한다
    //여기서 그런 버튼눌렀을 때 발생하는 기능들을 압축해서 객채{key.value}기능들을 모아놓은 것을 
    //바로 e라고 한다
    e.preventDefault();
    if(validateForm()==true){
        console.log("모든 필드가 유효합니다. 즉 사용이 가능합니다");
    }else{
        console.log("위 필드중 일부분이 에러가 터집니다. 유효성검사 실패");
    }
    //이거를 써줘야지 유효성검사 가능
    //기본적으로 폼태그에서 submit버튼을 누르면 자동수행되는 기능이 있고 폼제출동작을 막는다
    //폼제출동작은 자동수행되는 기능이있는데, 새로고침이다 =>console에 있던 데이터들이 사라진다
    //인풋태그의 에러확인(유효성검사)이 불가능해진다
});

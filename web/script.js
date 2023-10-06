// 初期化、API等のデータ取得
$.get( './initialization').done(function( data ) {
  if(data["OpenAI_API_KYE"]){
    $("#OpenAI_API_KEY_status").text("API Key 設定済み");
    $("#OpenAI_API_KEY_status").css( 'background-color', '#9C99F2' );
  }else{
    $("#OpenAI_API_KEY_status").text("API Key 未設定");
    $("#OpenAI_API_KEY_status").css( 'background-color', '#ff5555' );
  };
});
// APIKey送信
$('#API_form').submit(function() {
  $.ajax({"type":"post","url":"./API_KEY","data":JSON.stringify({"key":$('#OpenAI_API_KEY').val()}),
          "contentType":'application/json',"dataType":"json",
          "success":function(json_data){
              if(json_data["SetAPI"]){
                $("#OpenAI_API_KEY_status").text("API Key 設定済み");
                $("#OpenAI_API_KEY_status").css( 'background-color', '#9C99F2' );
              }else{
                $("#OpenAI_API_KEY_status").text("API Key 未設定");
                $("#OpenAI_API_KEY_status").css( 'background-color', '#ff5555' );
              }
            },
          "error":function(){
            alert("Server Error. Please try again later.");
          }});
  $('#OpenAI_API_KEY').val("")
});
// 英語入力用のinputのサイズ制御
function flexTextarea(el) {
  const dummy = el.querySelector('.FlexTextarea__dummy')
  el.querySelector('.FlexTextarea__textarea').addEventListener('input', e => {
    dummy.textContent = e.target.value + '\u200b'
  })
}

document.querySelectorAll('.FlexTextarea').forEach(flexTextarea)
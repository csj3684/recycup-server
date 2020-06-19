<script src="https://t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
<script>
    // 지도를 생성합니다
    var map = new kakao.maps.Map(mapContainer, mapOption);

    // 주소-좌표 변환 객체를 생성합니다
    var geocoder = new kakao.maps.services.Geocoder();


    new daum.Postcode({
        oncomplete: function(data) {
            if(data.userSelectedType=="R"){
                / 주소로 좌표를 검색합니다
                geocoder.addressSearch(data.roadAddress, function(result, status) {

                    // 정상적으로 검색이 완료됐으면
                     if (status === kakao.maps.services.Status.OK) {


                        window.TestApp.setAddress(result[0].y, result[0].x);
                    }
                });

            }
            else{
                geocoder.addressSearch(data.jibunAddress, function(result, status) {

                    // 정상적으로 검색이 완료됐으면
                     if (status === kakao.maps.services.Status.OK) {

                        window.TestApp.setAddress(result[0].y, result[0].x);


                    }
                });

            }
        }
    }).open();


</script>
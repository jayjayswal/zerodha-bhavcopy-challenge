var app = angular.module("web-app", []);
app.controller("form-controller", function($scope,$http) {

    $scope.top_stock_url="/get_top_stocks/"
    $scope.search_stock_url="/get_stock_by_name/"
    $scope.get_latest_stocks="/get_latest_stocks/"
    $scope.search_text=""
    $scope.eq_bhav_date=""
    $scope.top_stocks=[]
    $scope.search_stocks=[]

    /*
        Calls when page gets loaded.
    */
    $scope.setupApp=function(){
        $scope.getTopSocks(0,true)
    }

    /*
        Get top stacks for provided page number.
    */
    $scope.getTopSocks=function(pageNumber,firstTime){
        $http({
            method : "GET",
            url : $scope.top_stock_url+pageNumber
        })
        .then( function mySuccess(response) {
           console.log(response)
           response=response.data
           if(response.status == 1){
                if(response.data.length==0){
                    $scope.showError("No data found, Try to load bhavcopy again.");
                    return;
                }
                if(firstTime){
                    $scope.total_rows=response.count
                    $scope.setupPagination()
                    $scope.eq_bhav_date=response.date
                }
                $scope.top_stocks=response.data
           }
           else{
               $scope.showError(response.data);
           }
        }, function myError(response) {
           if(response.status == 500){
                $scope.serverError()
           }else if(response.status == 403){
                $scope.unAuthenticatedRequest()
           }
        });
    }

    /*
        Setup pagination for top stacks.
    */
    $scope.setupPagination=function(){
        $("#paginations").pagination({
            pageSize: 10,
            dataSource: function (done) {
                var result = [];
                for (var i = 1; i <= $scope.total_rows; i++) {
                    result.push(i);
                }
                done(result);
            },
            callback: function (data, pagination) {
                  $scope.getTopSocks(pagination.pageNumber-1,false)
            },
            className: 'paginarowtionjs-theme-red paginationjs-big'
        });
    }

    /*
        Search stock by name pattern
    */
    $scope.getStockByName=function(){
        $http({
            method : "GET",
            url : $scope.search_stock_url+$scope.search_text
        })
        .then( function mySuccess(response) {
           console.log(response)
           response=response.data
           if(response.status == 1){
                if(response.data.length==0){
                    $scope.showError("No data found, Try again with different query.");
                    return;
                }
                $scope.search_stocks=response.data
           }
           else{
               $scope.showError(response.data);
           }
        }, function myError(response) {
           if(response.status == 500){
                $scope.serverError()
           }else if(response.status == 403){
                $scope.unAuthenticatedRequest()
           }
        });
    }


    /*
        Reload latest bhavcopy to redis.
    */
    $scope.loadLatestData=function(){
         $http({
            method : "GET",
            url : $scope.get_latest_stocks
        })
        .then( function mySuccess(response) {
           console.log(response)
           response=response.data
           if(response.status == 1){
              $scope.showError(response.data);
              location.reload(true);
           }
           else{
               $scope.showError(response.data);
           }
        }, function myError(response) {
           if(response.status == 500){
                $scope.serverError()
           }else if(response.status == 403){
                $scope.unAuthenticatedRequest()
           }
        });
    }

    $scope.showError=function(msg){
        alert(msg)
    }

    $scope.serverError=function(){
        alert("Server Error, Try again after sometime.")
    }

    $scope.unAuthenticatedRequest=function(){
        alert("Unauthenticated Request.")
    }

});
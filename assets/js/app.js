var app = angular.module("web-app", []);
app.controller("form-controller", function($scope,$http) {

    $scope.top_stock_url="/get_top_stocks/"
    $scope.search_stock_url="/get_stock_by_name/"
    $scope.search_text=""

    $scope.setupApp=function(){
        $scope. getTopSocks(0,true)
    }

    $scope.getTopSocks=function(pageNumber,firstTime){
        $http({
            method : "GET",
            url : $scope.top_stock_url+pageNumber
        })
        .then( function mySuccess(response) {
           console.log(response)
           response=response.data
           if(response.status == 1){
                if(firstTime){
                    $scope.total_rows=response.count
                    $scope.setupPagination()
                }
                $scope.top_stocks=response.data
           }
           else{
               alert(response.data)
           }
        }, function myError(response) {
           if(response.status == 500){
                $scope.serverError()
           }else if(response.status == 403){
                $scope.unAuthenticatedRequest()
           }
        });
    }

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

    $scope.getStockByName=function(){
        $http({
            method : "GET",
            url : $scope.search_stock_url+$scope.search_text
        })
        .then( function mySuccess(response) {
           console.log(response)
           response=response.data
           if(response.status == 1){
                $scope.search_stocks=response.data
           }
           else{
               alert(response.data)
           }
        }, function myError(response) {
           if(response.status == 500){
                $scope.serverError()
           }else if(response.status == 403){
                $scope.unAuthenticatedRequest()
           }
        });
    }



});
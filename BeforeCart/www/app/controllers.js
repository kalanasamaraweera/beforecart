(function () {
    "use strict";

    angular.module("myapp.controllers", [])

    .controller("appCtrl", ["$scope", function ($scope) {

        $scope.items = [
   { id: 1 },
   { id: 2 },
   { id: 3 },
   { id: 4 },
   { id: 5 },
   { id: 6 },
   { id: 7 }
  

        ];

        

        $scope.moveItem = function (item, fromIndex, toIndex) {
            $scope.items.splice(fromIndex, 1);
            $scope.items.splice(toIndex, 0, item);
        };


    }])

    //homeCtrl provides the logic for the home screen
    .controller("homeCtrl", ["$scope", "$state", function ($scope, $state) {
        $scope.refresh = function () {
            //refresh binding
            $scope.$broadcast("scroll.refreshComplete");
        };
    }])
         .controller("signupCtrl", ["$scope", "$state", function ($scope, $state) {
             $scope.refresh = function () {
                 //refresh binding
                 $scope.$broadcast("scroll.refreshComplete");
             };
         }])
        .controller("resetPwdCtrl", ["$scope", "$state", function ($scope, $state) {
            $scope.refresh = function () {
                //refresh binding
                $scope.$broadcast("scroll.refreshComplete");
            };
        }])
        .controller("beforeResetPwdCtrl", ["$scope", "$state", function ($scope, $state) {
            $scope.refresh = function () {
                //refresh binding
                $scope.$broadcast("scroll.refreshComplete");
            };
        }])
        .controller("mainCatelogCtrl", ["$scope", "$state", function ($scope, $state) {
            $scope.refresh = function () {
                //refresh binding
                $scope.$broadcast("scroll.refreshComplete");
            };
        }])
        

         .controller("changeAccountCtrl", ["$scope", "$state", function ($scope, $state) {
             $scope.refresh = function () {
                 //refresh binding
                 $scope.$broadcast("scroll.refreshComplete");
             };
         }])
        .controller("askFriendCtrl", ["$scope", "$state", function ($scope, $state) {
            $scope.refresh = function () {
                //refresh binding
                $scope.$broadcast("scroll.refreshComplete");
            };
        }])
        
        


    //errorCtrl managed the display of error messages bubbled up from other controllers, directives, myappService
    .controller("errorCtrl", ["$scope", "myappService", function ($scope, myappService) {
        //public properties that define the error message and if an error is present
        $scope.error = "";
        $scope.activeError = false;

        //function to dismiss an active error
        $scope.dismissError = function () {
            $scope.activeError = false;
        };

        //broadcast event to catch an error and display it in the error section
        $scope.$on("error", function (evt, val) {
            //set the error message and mark activeError to true
            $scope.error = val;
            $scope.activeError = true;

            //stop any waiting indicators (including scroll refreshes)
            myappService.wait(false);
            $scope.$broadcast("scroll.refreshComplete");

            //manually apply given the way this might bubble up async
            $scope.$apply();
        });
    }]);
})();
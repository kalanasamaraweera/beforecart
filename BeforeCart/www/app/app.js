(function () {
    "use strict";

    angular.module("myapp", ["ionic", "myapp.controllers", "myapp.services"])
        .run(function ($ionicPlatform) {
            $ionicPlatform.ready(function () {
                if (window.cordova && window.cordova.plugins && window.cordova.plugins.Keyboard) {
                    cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
                }
                if (window.StatusBar) {
                    StatusBar.styleDefault();
                }
            });
        })
        // All this does is allow the message
// to be sent when you tap return
.directive('input', function($timeout) {
    return {
        restrict: 'E',
        scope: {
            'returnClose': '=',
            'onReturn': '&',
            'onFocus': '&',
            'onBlur': '&'
        },
        link: function(scope, element, attr) {
            element.bind('focus', function(e) {
                if (scope.onFocus) {
                    $timeout(function() {
                        scope.onFocus();
                    });
                }
            });
            element.bind('blur', function(e) {
                if (scope.onBlur) {
                    $timeout(function() {
                        scope.onBlur();
                    });
                }
            });
            element.bind('keydown', function(e) {
                if (e.which == 13) {
                    if (scope.returnClose) element[0].blur();
                    if (scope.onReturn) {
                        $timeout(function() {
                            scope.onReturn();
                        });
                    }
                }
            });
        }
    }
})



        
        .config(function ($stateProvider, $urlRouterProvider) {
            $stateProvider
            .state("app", {
                url: "/app",
                abstract: true,
                templateUrl: "app/templates/view-menu.html",
                controller: "appCtrl"
            })
            .state("app.home", {
                url: "/home",
                templateUrl: "app/templates/view-home.html",
                controller: "homeCtrl"
            })
            .state("app.signup", {
                url: "/signup",
                templateUrl: "app/templates/view-signup.html",
                controller: "signupCtrl"
            })
            .state("app.resetPwd", {
                url: "/resetPwd",
                templateUrl: "app/templates/view-resetpassword.html",
                controller: "resetPwdCtrl"
            })
             .state("app.beforeResetPwd", {
                 url: "/beforeResetPwd",
                 templateUrl: "app/templates/view-beforeresetpwd.html",
                 controller: "beforeResetPwdCtrl"
             })
                
            .state("app.mainCatelog", {
                url: "/mainCatelog",
                templateUrl: "app/templates/view-maincatelog.html",
                controller: "mainCatelogCtrl"
            })
            .state("app.askfriend", {
                url: "/askfriend",
                templateUrl: "app/templates/view-suggested-friendlist.html",
                controller: "askFriendCtrl"
            })

            .state('app.changeAccount', {
                url: '/changeAccount',
               
                templateUrl: 'app/templates/view-account-settings.html',
                controller: "changeAccountCtrl"
            })

            .state('app.chatView', {
                url: '/chatView',
               
                templateUrl: 'app/templates/view-chatview.html',
                controller: "chatViewCtrl"
            });


            $urlRouterProvider.otherwise("/app/home");
        });

    
})();
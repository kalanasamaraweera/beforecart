﻿(function () {
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

            .state('app.changeAccount', {
                url: '/changeAccount',
               
                templateUrl: 'app/templates/view-account-settings.html',
                controller: "changeAccountCtrl"
            });


            $urlRouterProvider.otherwise("/app/home");
        });
    
})();
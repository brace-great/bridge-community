import { LocalStorage, SessionStorage } from "quasar";
import { useStore } from "stores/bridge";
import { getUtils, putUtils } from "boot/utils";

const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/IndexPage.vue") },
      {
        path: "search/:keyword",
        component: () => import("pages/SearchPage.vue"),
      },
      {
        path: "reporthandling",
        component: () => import("pages/ReportHandling.vue"),
        beforeEnter: (to, from, next) => {
          if (useStore().user.is_superuser) {
            next();
          } else {
            alert("非管理员用户");
            next("/");
          }
        },
      },
    ],
  },
  {
    path: "/auth",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/AuthPart.vue") },
      {
        path: "forgotpassword",
        component: () => import("pages/ForgotPassword.vue"),
      },
      {
        path: "forgotpasswordconfirm/:uid/:token",
        component: () => import("pages/ForgotPasswordConfirm.vue"),
      },
    ],
    beforeEnter: (to, from, next) => {
      if (LocalStorage.getItem("access")) {
        alert("已登陆");
        next(from);
      } else {
        next();
      }
    },
  },
  {
    path: "/user",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: ":username", component: () => import("pages/UserData.vue") },
      {
        path: ":username/settings",
        component: () => import("pages/UserSettings.vue"),
      },
      {
        path: ":username/settings/password",
        component: () => import("pages/UserPwSettings.vue"),
      },
      {
        path: ":username/settings/email",
        component: () => import("pages/UserEmailSettings.vue"),
      },
      {
        path: ":username/notify",
        component: () => import("pages/UserNotify.vue"),
        beforeEnter: (to, from, next) => {
          putUtils(
            process.env.API + "wu/notify/",
            { username: useStore().user.username },
            true
          ).then((res) => {
            next();
          });
        },
      },
      {
        path: ":username/chat",
        component: () => import("pages/UserChat.vue"),
      },
      {
        path: ":username/newdiscuss",
        component: () => import("pages/NewDiscuss.vue"),
      },
    ],
    beforeEnter: (to, from, next) => {
      // authkey 存在 进入该路由，不存在跳转到登陆页面
      if (LocalStorage.getItem("access")) {
        next();
      } else {
        alert("请先登陆");
        next("/auth");
      }
    },
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;

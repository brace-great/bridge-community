import { defineStore } from "pinia";
import { SessionStorage, LocalStorage } from "quasar";

export const useStore = defineStore("bridge", {
  state: () => ({
    chat: SessionStorage.getItem("chat") || {},
    notify: SessionStorage.getItem("notify") || {},
    unread: SessionStorage.getItem("unread") || {},
    user: LocalStorage.getItem("user") || {},
    avatar: LocalStorage.getItem("avatar") || {},
  }),
  getters: {},
  actions: {
    setChat(chat) {
      SessionStorage.set("chat", chat);
      this.chat = chat;
    },
    setNotify(notify) {
      SessionStorage.set("notify", notify);
      this.notify = notify;
    },
    setUnread(unread) {
      SessionStorage.set("unread", unread);
      this.unread = unread;
    },
    setUser(user) {
      LocalStorage.set("user", user);
      this.user = user;
    },
    setAvatar(avatar) {
      LocalStorage.set("avatar", avatar);
      this.avatar = avatar;
    },
  },
});

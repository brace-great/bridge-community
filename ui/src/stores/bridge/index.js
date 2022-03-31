import { defineStore } from "pinia";
import { SessionStorage, LocalStorage } from "quasar";

export const useStore = defineStore("bridge", {
  state: () => ({
    chat: SessionStorage.getItem("chat") || {},
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

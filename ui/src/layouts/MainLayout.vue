<template>
  <q-layout view="hHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title class="row justify-between">
          <q-btn flat label="Bridge" to="/" />
          <q-input
            style="margin: auto"
            dark
            dense
            standout
            v-model="text"
            input-class="text-right"
            class="q-ml-md"
          >
            <template v-slot:append>
              <q-icon v-if="text === ''" name="search" />
              <q-icon
                v-else
                name="clear"
                class="cursor-pointer"
                @click="text = ''"
              />
            </template>
          </q-input>
        </q-toolbar-title>
        <!-- <q-btn icon="item" @click="trigger"> </q-btn> -->
        <q-btn
          v-if="access"
          flat
          dense
          round
          icon="logout"
          aria-label="auth"
          @click="signOut"
          ><q-tooltip class="bg-accent">退出登录</q-tooltip></q-btn
        >
        <q-btn
          v-if="!access"
          flat
          dense
          round
          icon="account_circle"
          aria-label="auth"
          to="/auth"
        />
      </q-toolbar>
    </q-header>

    <q-drawer
      width="200"
      class=""
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref, reactive } from "vue";
import EssentialLink from "components/EssentialLink.vue";
import { useRouter, useRoute } from "vue-router";
import { LocalStorage, SessionStorage } from "quasar";
import { getUtils as get } from "boot/utils";
import { useStore } from "stores/bridge";

export default defineComponent({
  name: "MainLayout",

  components: {
    EssentialLink,
  },

  setup() {
    const leftDrawerOpen = ref(false);
    let access = ref(LocalStorage.getItem("access"));
    const router = useRouter();
    const user = useStore().user;

    const chatBadge = ref(null);
    const store = useStore();
    if (access.value) {
      get(process.env.API + "wu/chatmessage/", true).then((res) => {
        let chat = res.data.results;
        for (const i in chat) {
          if (chat[i].receiver != user.username) {
            chat[i].group = chat[i].receiver;
          } else if (chat[i].sender != user.username) {
            chat[i].group = chat[i].sender;
          }
        }
        const listGroupUnread = ref({});
        const list = ref({});
        chatBadge.value = 0;
        for (const i in chat) {
          if (!list.value[chat[i].group]) {
            list.value[chat[i].group] = [];
          }
          list.value[chat[i].group].push(chat[i]);
          if (
            chat[i].isread_receiver == 0 &&
            chat[i].receiver == user.username
          ) {
            if (!listGroupUnread.value[chat[i].group]) {
              listGroupUnread.value[chat[i].group] = 0;
            }
            listGroupUnread.value[chat[i].group] += 1;
            chatBadge.value++;
          }
          if (chatBadge.value == 0) {
            chatBadge.value = null;
          }
        }

        store.setChat(list.value);
        store.setUnread(listGroupUnread.value);
      });
    } else {
      const chatBadge = ref(null);
    }
    const signOut = () => {
      LocalStorage.remove("access");
      LocalStorage.remove("refresh");
      router.push({
        path: "/auth/",
      });
      window.location.reload();
    };
    const linksList = [
      {
        title: "主页",
        link: "/",
      },
      {
        title: "通知",
        link: "user/" + LocalStorage.getItem("user").username + "/notify/",
        badge: ref(1),
      },
      {
        title: "私信",
        link: "user/" + LocalStorage.getItem("user").username + "/chat/",
        badge: chatBadge,
      },
      {
        title: "个人动态",
        link: "user/" + LocalStorage.getItem("user").username,
      },
      {
        title: "设置",
        link: "user/" + LocalStorage.getItem("user").username + "/settings/",
      },
    ];
    const bar = ref(null);

    // we manually trigger it (this is not needed if we
    // don't skip Ajax calls hijacking)

    return {
      bar,
      text: ref(""),
      access,
      signOut,
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },
});
</script>

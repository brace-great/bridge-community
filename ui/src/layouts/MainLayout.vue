<template>
  <q-layout view="hHh LpR lFf">
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
          <q-btn
            flat
            label="发布新讨论"
            :to="'/user/' + store.user.username + '/newdiscuss'"
            style="margin-left: 50px"
          />
          <div class="row" style="margin: auto">
            <q-input
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
            <q-btn :to="'/search/' + text" label="搜索" flat />
          </div>
        </q-toolbar-title>
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
      :width="width"
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
import { defineComponent, onBeforeMount, ref, reactive } from "vue";
import EssentialLink from "components/EssentialLink.vue";
import { useRouter, useRoute } from "vue-router";
import { LocalStorage, SessionStorage } from "quasar";
import { getUtils } from "boot/utils";
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
    const notifyBadge = ref(null);
    const store = useStore();
    const linkusername = ref("");
    onBeforeMount(async () => {
      if (access.value) {
        const res = await getUtils(process.env.API + "wu/notify/", true);
        store.setNotify(res.data.results.reverse());
        notifyBadge.value = 0;
        for (const i in store.notify) {
          if (store.notify[i].isread == 0) {
            notifyBadge.value += 1;
          }
        }
        if (notifyBadge.value == 0) {
          notifyBadge.value = null;
        }
      }
    });

    if (user) {
      linkusername.value = user.username;
    }
    if (access.value) {
      getUtils(process.env.API + "wu/chatmessage/", true).then((res) => {
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
    };
    let linksList = [
      {
        title: "主页",
        link: "/",
      },
      {
        title: "通知",
        link: "/user/" + linkusername.value + "/notify/",
        badge: notifyBadge,
      },
      {
        title: "私信",
        link: "/user/" + linkusername.value + "/chat/",
        badge: chatBadge,
      },
      {
        title: "个人动态",
        link: "/user/" + linkusername.value,
      },
      {
        title: "设置",
        link: "/user/" + linkusername.value + "/settings/",
      },
    ];
    if (store.user.is_superuser) {
      linksList.push({ title: "管理员后台", link: "/reporthandling/" });
    }
    const bar = ref(null);

    // we manually trigger it (this is not needed if we
    // don't skip Ajax calls hijacking)

    return {
      notifyBadge,
      width: ref(200),
      store,
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

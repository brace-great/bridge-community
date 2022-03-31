<template>
  <q-page class="fit row reverse wrap">
    <q-list bordered separator class="content-center col-2">
      <q-item
        clickable
        v-ripple
        v-for="i in store.chat"
        :key="i"
        @click="clickItem(i[0]['group'])"
      >
        <q-item-section avatar>
          <q-avatar size="" class="offset-1">
            <img :src="store.avatar[i[0]['group']]" />
          </q-avatar>
        </q-item-section>
        <q-item-section>
          <q-item-label class="row justify-between">
            {{ i[0]["group"] }}
            <q-badge
              rounded
              color="red"
              v-bind:label="store.unread[i[0]['group']]"
              v-if="store.unread[i[0]['group']]"
          /></q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
    <div class="col-10 column reverse" style="min-height: 90vh" v-if="detail">
      <div class="">
        <q-input v-model="text" filled autogrow>
          <template v-slot:append>
            <q-btn label="发送" @click="send" name="search" /> </template
        ></q-input>
      </div>
      <div class="">
        <q-chat-message
          class=""
          v-for="(i, index) in store.chat[detail]"
          :key="i.sender != username ? i.isshow_receiver : i.isshow_sender"
          v-show="i.sender != username ? i.isshow_receiver : i.isshow_sender"
          :stamp="i.time"
          :sent="i.sender != username ? false : true"
        >
          <template v-slot:avatar>
            <q-avatar size="">
              <img
                class="cursor-pointer"
                @click="toUserData(i.sender)"
                :src="i.sender != username ? store.avatar[i.sender] : myAvatar"
              />
            </q-avatar>
          </template>
          <q-chip
            removable
            color="teal"
            text-color="white"
            @remove="
              deleteMessage(
                i.id,
                i.sender != username ? 'isshow_receiver' : 'isshow_sender',
                index
              )
            "
          >
            {{ i.text }}
          </q-chip>
        </q-chat-message>
      </div>
    </div>
  </q-page>
</template>

<script>
import {
  defineComponent,
  ref,
  reactive,
  onBeforeMount,
  onMounted,
  onActivated,
  onUpdated,
} from "vue";
import { getUtils as get, patchUtils, putUtils, postUtils } from "boot/utils";
import { useStore } from "stores/bridge";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "UserChat",

  setup() {
    const store = useStore();
    // const list = ref(store.chat);
    const detail = ref(false);
    const router = useRouter();
    const username = store.user.username;
    const myAvatar = ref();
    const text = ref("");
    get(process.env.API + "wu/userinfos/" + username, false).then((res) => {
      myAvatar.value = res.data.avatar;
    });
    for (const i in store.chat) {
      get(process.env.API + "wu/userinfos/" + i, false).then((res) => {
        store.avatar[i] = res.data.avatar;
      });
    }

    store.setAvatar(store.avatar);

    return {
      // list: list,

      username,
      myAvatar,
      text,
      eclair: ref(true),

      detail,
      store,
      toUserData(username) {
        router.push("/user/" + username);
      },
      deleteMessage(id, showfor, index) {
        let data = {};
        data[showfor] = 0;
        patchUtils(process.env.API + "wu/chatmessage/" + id + "/", data).then(
          (res) => {}
        );
        store.chat[detail.value][index][showfor] = 0;
        store.setChat(store.chat);
      },
      send() {
        if (text.value) {
          let postData = {
            sender: username,
            receiver: detail.value,
            text: text.value,
            isshow_receiver: 1,
            isread_receiver: 0,
            isshow_sender: 1,
          };
          postUtils(process.env.API + "wu/chatmessage/", postData, true).then(
            (res) => {
              text.value = "";
              store.chat[detail.value].push(res.data);
              store.setChat(store.chat);
            }
          );
        }
      },

      clickItem(name) {
        detail.value = name;
        if (store.unread[name]) {
          putUtils(
            process.env.API + "wu/chatmessage/",
            {
              sender: name,
            },
            true
          ).then((res) => {
            store.unread[name] = 0;
            store.setUnread(store.unread);
          });
        }
      },
    };
  },
});
</script>

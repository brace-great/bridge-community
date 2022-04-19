<template>
  <q-page class="row wrap">
    <q-list style="padding-top: 5px" separator class="content-center">
      <div v-for="(i, index) in discuss" :key="index">
        <q-item clickable @click="changeFlag(index)">
          <q-item-section top avatar class="column items-center">
            <q-avatar size="" class="">
              <img :src="avatars[i.starter]" @click="toUserData(i.starter)" />
            </q-avatar>
            {{ i.starter }}
          </q-item-section>

          <q-item-section>
            <q-item-label
              style="font-size: large"
              class="row items-center justify-between"
              >{{ i.title }}
              <div class="row">
                <div
                  style="margin: 10px; font-size: small"
                  v-for="j in tags[i.title]"
                  :key="j"
                >
                  {{ "#" + j }}
                </div>
              </div>
            </q-item-label>
            <q-item-label caption :lines="lines[index]">
              {{ i.text }}
            </q-item-label>
          </q-item-section>

          <q-item-section side top class="column">
            <q-item-label caption>{{ i.time }}</q-item-label>
            <q-btn
              label="展开"
              color="primary"
              style="margin-top: 15px"
              @click="expand(index)"
              v-show="lines[index] == 2"
            />
            <q-btn
              label="收回"
              color="primary"
              style="margin-top: 15px"
              @click="reclaim(index)"
              v-show="lines[index] != 2"
            />
            <q-btn
              label="收回"
              color="primary"
              style="margin-top: auto"
              @click="reclaim(index)"
              v-show="lines[index] != 2"
            />
          </q-item-section>
        </q-item>

        <q-separator spaced inset="item" />
      </div>
    </q-list>

    <q-drawer
      show-if-above
      class="column reverse justify-between"
      side="right"
      :width="width"
      bordered
      ><div class="row">
        <q-input
          v-model="rightdowntext"
          class="col-grow"
          filled
          type="textarea"
        />
        <q-btn
          label="发送"
          color="primary"
          style="margin-top: 15px"
          flat
          @click="sendComment()"
        ></q-btn>
      </div>
      <q-scroll-area class="col-grow" style="max-width: 100%">
        <div
          v-if="!comments[flag]"
          style="text-align: center; margin-top: 10px"
        >
          -- 还没有人参与此讨论 --
        </div>
        <div v-for="(i, index) in comments[flag]" :key="index" class="">
          <q-item>
            <q-item-section>
              <q-item-label
                >{{ i.commenter }} <b v-show="i.replyto">回复</b
                ><i v-show="i.replyto">{{ i.replyto }}</i>
              </q-item-label>
              <q-item-label caption>{{ i.text }}</q-item-label>
            </q-item-section>

            <q-item-section side top>
              <q-item-label caption>{{ i.time }}</q-item-label>
              <q-btn push color="primary" label="回复" style="margin-top: 10px">
                <q-popup-edit
                  v-model="replyvalue"
                  auto-save
                  v-slot="replyvalue2"
                >
                  <q-input v-model="replyvalue2.value" dense autofocus counter
                    ><template v-slot:append>
                      <q-btn
                        label="发送"
                        @click="reply(replyvalue2, i.id)"
                      /> </template
                  ></q-input>
                </q-popup-edit>
              </q-btn>
            </q-item-section>
          </q-item>
          <q-separator spaced inset />
        </div>
      </q-scroll-area>
    </q-drawer>
  </q-page>
</template>

<script>
import { getUtils, postUtils, putUtils } from "src/boot/utils";
import { defineComponent, ref, onBeforeMount } from "vue";
import { useStore } from "stores/bridge";
import { useRouter, useRoute } from "vue-router";
import { useQuasar } from "quasar";
import { set } from "vue-demi";

export default defineComponent({
  name: "SearchPage",
  setup() {
    const store = useStore();
    const discuss = ref({});
    const rightdowntext = ref();
    const replyvalue = ref("");
    const comments = ref({});
    const flag = ref();
    const avatars = ref(store.avatar);
    const lines = ref([]);
    const tags = ref({});
    const router = useRouter();
    const route = useRoute();
    const $q = useQuasar();
    const getDiscussData = async () => {
      const res = await putUtils(process.env.API + "wu/discusswithtag/", {
        keyword: route.params.keyword,
      });
      const tem = res.data.discuss.reverse();
      const tem2 = res.data.comments.reverse();

      for (const i in tem) {
        if (i == 0) {
          flag.value = tem[i].title;
        }
        discuss.value[tem[i]["title"]] = tem[i];
        if (!tags.value[tem[i]["title"]]) {
          tags.value[tem[i]["title"]] = new Set();
        }
        tags.value[tem[i]["title"]].add(tem[i]["tag"]);
        if (!comments.value[tem[i]["title"]]) {
          comments.value[tem[i]["title"]] = new Set();
        }
        tem2.forEach((element) => {
          if (element.discuss == tem[i]["id"]) {
            comments.value[tem[i]["title"]].add(element);
          }
        });
        if (comments.value[tem[i]["title"]].size == 0) {
          comments.value[tem[i]["title"]] = null;
        }
      }
    };
    onBeforeMount(async () => {
      await getDiscussData();
      console.log("comments", comments.value);

      for (const i in discuss.value) {
        lines.value[i] = 2;
        if (!avatars.value[discuss.value[i].starter]) {
          getUtils(
            process.env.API + "wu/userinfos/" + discuss.value[i].starter,
            false
          ).then((res) => {
            avatars.value[discuss.value[i].starter] = res.data.avatar;
            store.setAvatar(avatars.value);
          });
        }
      }
    });

    return {
      width: ref(500),
      replyvalue,
      flag,
      discuss,
      comments,
      avatars,
      lines,
      tags,
      rightdowntext,
      async sendComment() {
        const res = await postUtils(
          process.env.API + "wu/comment/",
          {
            discuss: discuss.value[flag.value].id,
            commenter: store.user.username,
            text: rightdowntext.value,
          },
          true
        );
        if (res.status == 201) {
          $q.notify({
            color: "positive",
            textColor: "white",
            message: "回复成功",
          });
          await getDiscussData();
        } else {
          $q.notify({
            color: "negative",
            textColor: "white",
            message: "回复失败",
          });
        }
        rightdowntext.value = "";
      },
      async reply(text, replyto_id) {
        const res = await postUtils(
          process.env.API + "wu/comment/",
          {
            discuss: discuss.value[flag.value].id,
            replyto: replyto_id,
            commenter: store.user.username,
            text: text.value,
          },
          true
        );

        if (res.status == 201) {
          $q.notify({
            color: "positive",
            textColor: "white",
            message: "回复成功",
          });
          await getDiscussData();
        } else {
          $q.notify({
            color: "negative",
            textColor: "white",
            message: "回复失败",
          });
        }
        text.value = "";
      },
      expand(index) {
        lines.value[index] = "";
      },
      reclaim(index) {
        lines.value[index] = 2;
      },
      toUserData(username) {
        router.push("/user/" + username);
      },
      changeFlag(index) {
        flag.value = index;
      },
    };
  },
});
</script>

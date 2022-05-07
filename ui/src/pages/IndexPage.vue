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
                  v-for="j in i.tags"
                  :key="j"
                >
                  {{ "#" + j }}
                </div>
              </div>
            </q-item-label>
            <q-item-label
              style="white-space: pre-wrap"
              caption
              :lines="lines[index]"
            >
              {{ i.text }}
            </q-item-label>
          </q-item-section>

          <q-item-section side top class="column">
            <q-item-label caption
              >{{ i.time
              }}<q-icon name="more_vert">
                <q-menu touch-position>
                  <q-list style="">
                    <q-item
                      clickable
                      v-close-popup
                      @click="showReport(i.starter, 'discuss', i.id, i.text)"
                    >
                      <q-item-section>举报</q-item-section>
                    </q-item>
                  </q-list>
                </q-menu>
              </q-icon></q-item-label
            >
            <div>
              <q-btn
                label="撤回"
                color="primary"
                style="margin-top: 15px"
                v-show="store.user.is_superuser"
                @click="withdraw(i.id, 'discuss')"
              />
              <q-btn
                label="展开"
                color="primary"
                style="margin-top: 15px"
                @click="expand(index)"
                v-show="lines[index] == 2"
              />
            </div>
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
              v-show="lines[index] != 2 && i.text.length > 1000"
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
              <q-item-label caption
                >{{ i.time
                }}<q-icon name="more_vert">
                  <q-menu touch-position>
                    <q-list style="">
                      <q-item
                        clickable
                        v-close-popup
                        @click="
                          showReport(i.commenter, 'comment', i.id, i.text)
                        "
                      >
                        <q-item-section>举报</q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                </q-icon></q-item-label
              >
              <div>
                <q-btn
                  label="撤回"
                  color="primary"
                  style="margin-top: 10px"
                  v-show="store.user.is_superuser"
                  @click="withdraw(i.id, 'comment')"
                />
                <q-btn
                  push
                  color="primary"
                  label="回复"
                  style="margin-top: 10px"
                >
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
              </div>
            </q-item-section>
          </q-item>
          <q-separator spaced inset />
        </div>
      </q-scroll-area>
    </q-drawer>
    <q-dialog v-model="report" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <span class="q-ml-sm">请输入举报理由</span>
        </q-card-section>
        <q-card-section class="row items-center">
          <q-input
            dense
            v-model="reason"
            autofocus
            @keyup.enter="report = false"
            style="width: 700px; max-width: 80vw"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="取消" color="primary" v-close-popup />
          <q-btn
            flat
            label="确认"
            color="primary"
            @click="sendReport"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { getUtils, postUtils, patchUtils } from "src/boot/utils";
import { defineComponent, ref, onBeforeMount } from "vue";
import { useStore } from "stores/bridge";
import { useRouter } from "vue-router";
import { useQuasar } from "quasar";

export default defineComponent({
  name: "IndexPage",
  setup() {
    const store = useStore();
    const discuss = ref();
    const rightdowntext = ref();
    const replyvalue = ref("");
    const comments = ref([]);
    const flag = ref(0);
    const avatars = ref(store.avatar);
    const lines = ref([]);
    const router = useRouter();
    const $q = useQuasar();
    const report = ref(false);
    const reportData = ref({ owner: "", type: "", id: -1, text: "" });
    const reason = ref("");
    const showReport = (owner, type, id, text) => {
      report.value = true;
      reportData.value.owner = owner;
      reportData.value.type = type;
      reportData.value.id = id;
      reportData.value.text = text;
    };
    const getDiscussData = async () => {
      const res = await getUtils(process.env.API + "wu/discuss/");
      discuss.value = res.data.results.reverse();
      for (const i in discuss.value) {
        discuss.value[i].text = discuss.value[i].text.replace(/<br>/g, "\n");
        comments.value[i] = discuss.value[i].comments;
        if (comments.value[i].length == 0) {
          comments.value[i] = null;
        }
      }
    };
    onBeforeMount(async () => {
      await getDiscussData();

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
      showReport,
      reason,
      report,
      replyvalue,
      flag,
      discuss,
      comments,
      avatars,
      lines,
      rightdowntext,
      store,

      async withdraw(id, type) {
        if (type == "discuss") {
          const res = await patchUtils(
            process.env.API + "wu/discuss/" + id + "/",
            {
              isshow: 0,
            }
          );
          if (res.status == 200) {
            await getDiscussData();
          } else {
            $q.dialog.alert({
              message: res.data.msg,
              color: "negative",
            });
          }
        } else {
          const res = await patchUtils(
            process.env.API + "wu/comment/" + id + "/",
            {
              notshow: 1,
            }
          );
          if (res.status == 201) {
            await getDiscussData();
          } else {
            $q.dialog.alert({
              message: res.data.msg,
              color: "negative",
            });
          }
        }
      },
      async sendReport() {
        const res = await postUtils(
          process.env.API + "wu/report/",
          {
            username: reportData.value.owner,
            content_type: reportData.value.type,
            content_id: reportData.value.id,
            content_text: reportData.value.text,
            reason: reason.value,
            reporter: store.user.username,
          },
          true
        );
        if (res.status == 201) {
          $q.notify({
            color: "positive",
            textColor: "white",
            message: "举报成功",
          });
        } else {
          $q.notify({
            color: "negative",
            textColor: "white",
            message: "未知错误",
          });
        }
      },
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

<template>
  <div id="databox">
    <div class="dataheader">
      <!-- <div class="firstheader"></div> -->
      <!-- 添加及搜索 -->
      <div class="secondheader" style="width:100%">
        <el-form :rules="rules" ref="headerForm" :inline="true" class="demo-ruleForm">
          <el-form-item label="所属日期" class="timeStyle">
            <el-date-picker
              :disabled="boolStatus"
              type="date"
              placeholder="选择日期"
              v-model="timeChange"
              value-format="yyyy-MM-dd"
              format="yyyy-MM-dd"
              :picker-options="pickerOptions"
              @change="timePutChange"
            >></el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click.native.prevent="addData">添加记录</el-button>
          </el-form-item>
          <el-form-item>
            <el-input
              placeholder="请输入内容"
              v-model.trim="searchContext"
              class="input-with-select"
              style="width:600px"
              clearable
              @change="serchPutChange"
            >
              <el-select v-model="searchData" slot="prepend" placeholder="请选择" style="width:150px">
                <el-option label="订单号" value="1"></el-option>
                <el-option label="会员账号" value="2"></el-option>
                <el-option label="真实姓名" value="3"></el-option>
                <el-option label="对应金额" value="4"></el-option>
                <el-option label="银行卡号" value="5"></el-option>
              </el-select>
              <el-button
                slot="append"
                icon="el-icon-search"
                class="searchIconStyle"
                @click.native.prevent="searchBtnControl"
              ></el-button>
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <hr />
    </div>

    <div class="datamain">
      <!-- 弹窗对话框  -->
      <el-dialog
        :title="title==='NEW'?'添加记录':'编辑记录'"
        :visible.sync="dialogFormVisible"
        :before-close="handleClose"
        :close-on-click-modal="false"
        top="1vh"
        width="550px"
      >
        <el-form :model="dialogform" ref="ruleForm" :rules="rules">
          <el-form-item
            label="所属银行"
            :label-width="formLabelWidth"
            prop="cardclass"
            class="amountStyle"
          >
            <el-input
              v-model.trim="dialogform.cardclass"
              autocomplete="off"
              clearable
              placeholder="请输入所属银行"
            ></el-input>
          </el-form-item>
          <el-form-item label="会员账号" :label-width="formLabelWidth" prop="account">
            <el-input
              v-model.trim="dialogform.account"
              autocomplete="off"
              clearable
              placeholder="请输入会员账号"
            ></el-input>
          </el-form-item>
          <el-form-item label="真实姓名" :label-width="formLabelWidth" prop="name" class="amountStyle">
            <el-input
              v-model.trim="dialogform.name"
              autocomplete="off"
              clearable
              placeholder="请输入真实姓名"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="对应金额"
            :label-width="formLabelWidth"
            prop="amount"
            class="amountStyle"
          >
            <el-input
              v-model.trim="dialogform.amount"
              autocomplete="off"
              clearable
              placeholder="请输入对应金额"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="银行卡号"
            :label-width="formLabelWidth"
            prop="cardnum"
            class="amountStyle"
          >
            <el-input
              v-model.trim="dialogform.cardnum"
              autocomplete="off"
              clearable
              placeholder="请输入银行卡号"
            ></el-input>
          </el-form-item>
          <el-form-item label="信息备注" :label-width="formLabelWidth">
            <el-input
              type="textarea"
              rows="3"
              placeholder="请输入备注"
              v-model.trim="dialogform.remark"
              clearable
            ></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native.prevent="cancel">取 消</el-button>
          <el-button type="primary" @click.native.prevent="confirm">确 定</el-button>
        </div>
      </el-dialog>

      <!-- 表格渲染 -->
      <el-table
        ref="tableForm"
        :data="tableData"
        style="width: 100%"
        :row-style="btnBackGround"
        border
      >
        <el-table-column label="日期" prop="date_group" fixed width="50px">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top">
              <p>{{ scope.row.date_group }}</p>
              <div slot="reference" class="name-wrapper" style="text-align:center">
                <i class="el-icon-time"></i>
              </div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="订单号" prop="onlyid" fixed width="80px">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top">
              <p>{{ scope.row.onlyid }}</p>
              <div slot="reference" class="name-wrapper">
                <el-tag size="medium">单号</el-tag>
              </div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="会员账号" prop="account" width="150px">
          <template slot-scope="scope">
            <div v-if="scope.row.remark!==''">
              <el-popover trigger="hover" placement="top">
                <p>备注：{{ scope.row.remark }}</p>
                <div slot="reference" class="name-wrapper">
                  <div style="color:#3c0ef7">{{ scope.row.account }}</div>
                </div>
              </el-popover>
            </div>
            <div v-else>{{ scope.row.account }}</div>
          </template>
        </el-table-column>
        <el-table-column label="真实姓名" prop="name" width="150px"></el-table-column>
        <el-table-column label="对应金额" prop="amount" width="150px"></el-table-column>
        <el-table-column label="所属银行" prop="cardclass" width="200px"></el-table-column>
        <el-table-column label="银行卡号" prop="cardnum" width="200px"></el-table-column>
        <el-table-column align="left" label="操作" fixed="right" width="220px">
          <template v-slot="scope">
            <div v-if="!scope.row.is_confirm">
              <div v-if="!scope.row.is_lock">
                <el-button
                  size="mini"
                  type="primary"
                  :class="{freezeStyle:scope.row.is_freeze}"
                  @click="handleStatus(scope.$index, scope.row,scope.row.is_freeze)"
                >{{scope.row.is_freeze?'解冻':'冻结'}}</el-button>
                <el-button
                  size="mini"
                  type="warning"
                  :disabled="!scope.row.is_freeze"
                  @click="handleEdit(scope.$index, scope.row)"
                >修改</el-button>
                <el-button
                  size="mini"
                  type="danger"
                  :disabled="!scope.row.is_freeze"
                  @click="handleDelete(scope.$index, scope.row)"
                >删除</el-button>
              </div>
              <div v-else>
                <i class="el-icon--right el-icon-loading"></i>
                数据处理中......
              </div>
            </div>
            <div v-else>
              <i class="el-icon--right el-icon-success"></i>
              已完成受理
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页及按钮 -->
    <div class="datafooter">
      <div class="btnStyle">
        <el-input
          v-model="totalSum"
          style="width:300px;vertical-align: top;color:#4d58dc;"
          size="small"
          class="totalSumStyle"
        >
          <template slot="prepend">总计：</template>
        </el-input>
        <el-input v-model="smallSum" style="width:300px;vertical-align: top;" size="small">
          <template slot="prepend">小计：</template>
        </el-input>
      </div>
      <div class="paginationStyle">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagin.currentPage"
          :page-sizes="pagin.pagesizes"
          :page-size="pagin.pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagin.total"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>
<script>
// 弹窗对话框初始值
const defaultDialogForm = {
  id: "",
  onlyid: "",
  cardclass: "",
  account: "",
  name: "",
  amount: "",
  cardnum: "",
  remark: "",
};

// 分页初始值
const defaultPagin = {
  currentPage: 1,
  pagesizes: [3, 20, 50],
  pagesize: 3,
  total: 0,
};

export default {
  data() {
    const cardclassVali = (rule, value, callback) => {
      const strVal = value.toString();
      if (strVal.length === 0) {
        return callback(new Error("请输入所属银行"));
      }
      const regTemp = /^[a-zA-Z\u4E00-\u9FA5\s]+$/;
      const res = strVal.match(regTemp);
      if (!res) {
        return callback(new Error("所属银行禁含有数字或非法字符"));
      }
      return callback();
    };
    const accountVali = (rule, value, callback) => {
      const strVal = value.toString();
      if (strVal.length === 0) {
        return callback(new Error("请输入会员账号"));
      }
      const regTemp = /^[^\u4E00-\u9FA5\s]+$/;
      const res = strVal.match(regTemp);
      if (!res) {
        return callback(new Error("会员账号禁含有汉字或空格"));
      }
      return callback();
    };
    const nameVali = (rule, value, callback) => {
      const strVal = value.toString();
      if (strVal.length === 0) {
        return callback(new Error("请输入真实姓名"));
      }
      const regTemp = /^[a-zA-Z\u4E00-\u9FA5\s]+$/;
      const res = strVal.match(regTemp);
      if (!res) {
        return callback(new Error("真实姓名禁含有数字或非法字符"));
      }
      return callback();
    };
    const amountVali = (rule, value, callback) => {
      const strVal = value.toString();
      if (strVal.length === 0) {
        return callback(new Error("请输入对应金额"));
      }
      const regTemp = /^[0-9]+$/;
      const res = strVal.match(regTemp);
      if (!res) {
        return callback(new Error("金额禁含有字母或负数或非法字符"));
      }
      if (parseInt(strVal) > 10000000) {
        return callback(new Error("金额仅限千万以内"));
      }
      return callback();
    };
    const cardnumVali = (rule, value, callback) => {
      const strVal = value.toString();
      if (strVal.length === 0) {
        return callback(new Error("请输入银行卡号"));
      }
      const regTemp = /^[0-9]+$/;
      const res = strVal.match(regTemp);
      if (!res) {
        return callback(new Error("银行卡号禁含有字母或负数或非法字符"));
      }
      if (strVal.length < 16 || strVal.length > 19) {
        return callback(new Error("银行卡号位数16到19之间"));
      }
      return callback();
    };
    return {
      // -----------添加及搜索-----------
      searchData: "",
      searchSetData: [],
      searchContext: "",
      paramsdict: {},
      timeChange: "",
      boolStatus: false,
      pickerOptions: {
        // disabledDate(time) {
        //   return time.getTime() + 3600 * 1000 * 24 * 7 < Date.now();
        // },
        shortcuts: [
          {
            text: "今天",
            onClick(picker) {
              picker.$emit("pick", new Date());
            },
          },
          {
            text: "昨天",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit("pick", date);
            },
          },
          {
            text: "一周前",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", date);
            },
          },
        ],
      },
      // ----------- 弹窗对话框-----------
      dialogFormVisible: false,
      title: "NEW",
      dialogform: Object.assign({}, defaultDialogForm),
      formLabelWidth: "80px",
      // ----------- 表格渲染-----------
      tableData: [],
      isActiveFreeze: true,
      // ----------- 分页-----------
      totalSum: "",
      smallSum: "",
      pagin: Object.assign({}, defaultPagin),
      // ----------- 验证-----------
      rules: {
        cardclass: [
          { required: true, validator: cardclassVali, trigger: "blur" },
        ],
        account: [{ required: true, validator: accountVali, trigger: "blur" }],
        name: [{ required: true, validator: nameVali, trigger: "blur" }],
        amount: [{ required: true, validator: amountVali, trigger: "blur" }],
        cardnum: [{ required: true, validator: cardnumVali, trigger: "blur" }],
      },
    };
  },
  methods: {
    // -----------添加及搜索-----------
    timePutChange(val) {
      this.pagin.currentPage = 1;
      this.boolStatus = true;
      this.getAllInfo();
    },
    // 添加目标
    addData() {
      if (!!this.timeChange) {
        this.title = "NEW";
        this.dialogform = Object.assign({}, defaultDialogForm);
        this.dialogFormVisible = true;
      } else {
        const h = this.$createElement;
        this.$notify({
          message: h(
            "b",
            { style: "color: #ef9206" },
            "请先选择-所属日期，才能添加记录"
          ),
          duration: 2000,
        });
        return false;
      }
    },
    // 搜索框没有值时触发
    serchPutChange(val) {
      let newVal = val.toString().trim();
      if (newVal == "") {
        this.pagin.currentPage = 1;
        this.getAllInfo();
      } else {
        return false;
      }
    },
    // 按下搜索时触发
    searchBtnControl() {
      if (!!this.searchData && !!this.searchContext && !!this.timeChange) {
        this.pagin.currentPage = 1;
        this.getAllInfo();
      } else {
        const h = this.$createElement;
        if (!this.timeChange) {
          this.$notify({
            message: h(
              "b",
              { style: "color: #ef9206" },
              "请先选择-所属日期，才能操作"
            ),
            duration: 2000,
          });
        } else if (!this.searchData) {
          this.$notify({
            message: h(
              "b",
              { style: "color: #ef9206" },
              "请先选择-搜索项目，才能操作"
            ),
            duration: 2000,
          });
        } else if (!this.searchContext) {
          this.$notify({
            message: h(
              "b",
              { style: "color: #ef9206" },
              "请输入搜索内容，才能操作"
            ),
            duration: 2000,
          });
        }
        return false;
      }
    },
    // ----------- 弹窗对话框-----------
    //点击对话框外面事件
    handleClose(done) {
      this.dialogFormVisible = false;
      this.$refs["ruleForm"].resetFields();
      done();
      return false;
    },
    // 确定送出
    confirm() {
      this.$refs["ruleForm"].validate((val) => {
        if (val) {
          this.dialogFormVisible = false;
          let newInfo = this.dialogform;
          newInfo["timeinfo"] = this.timeChange;
          let reqData = JSON.stringify(newInfo);
          if (this.title === "EDIT") {
            this.$store
              .dispatch("management/PutManagement", reqData)
              .then((response) => {
                this.getAllInfo();
                const { code, msg } = response;
                this.$message({
                  type:
                    code.toString().substr(0, 1) === "2" ? "success" : "error",
                  message: msg,
                });
              });
          } else {
            this.$store
              .dispatch("management/AddManagement", reqData)
              .then((response) => {
                this.getAllInfo();
                const { code, msg } = response;
                this.$message({
                  type:
                    code.toString().substr(0, 1) === "2" ? "success" : "error",
                  message: msg,
                });
              });
          }
        }
      });
    },
    // 取消对话框
    cancel() {
      this.dialogFormVisible = false;
      this.$refs["ruleForm"].resetFields();
    },
    // ----------- 表格渲染-----------
    // 获取所有目标
    getAllInfo() {
      this.paramsdict = Object.assign({},{})
      if (!this.timeChange) {
        return false;
      } else {
        this.paramsdict["timeinfo"] = this.timeChange;
      }
      if (!!this.searchData && !!this.searchContext) {
        this.paramsdict["searchgroup"] = this.searchData;
        this.paramsdict["searchcontext"] = this.searchContext;
      }
      if (
        (this.pagin.currentPage - 1) * this.pagin.pagesize ==
          this.pagin.total &&
        this.pagin.currentPage - 1 > 0
      ) {
        this.pagin.currentPage -= 1;
      }
      let dataInfo = {
        currentpage:
          this.pagin.currentPage === null ? 1 : this.pagin.currentPage,
        pagesize: this.pagin.pagesize,
      };

      if (!!this.paramsdict) {
        dataInfo["search"] = this.paramsdict;
      }
      this.$store
        .dispatch("management/GetManagement", dataInfo)
        .then((response) => {
          const { data, total, sum } = response;
          this.tableData = data;
          this.pagin.total = total;
          this.totalSum = sum;
          if (response.data.length > 0) {
            let items = response.data;
            let smallSum = 0;
            for (let i in items) {
              smallSum += items[i].amount;
            }
            this.smallSum = smallSum;
          }else{
            this.smallSum = ""
          }
        });
    },
    // 编辑
    handleEdit(index, row) {
      if (!row.is_freeze && row.is_confirm) {
        return false;
      }
      this.dialogform = Object.assign({}, defaultDialogForm);
      this.title = "EDIT";
      this.dialogFormVisible = true;
      this.dialogform.cardclass = row.cardclass;
      this.dialogform.account = row.account;
      this.dialogform.name = row.name;
      this.dialogform.amount = row.amount;
      this.dialogform.cardnum = row.cardnum;
      this.dialogform.remark = row.remark;
      this.dialogform.id = row.id;
      this.dialogform.onlyid = row.onlyid;
    },
    // 冻结
    handleStatus(index, row, sccc) {

      let data = {
        id: row.id,
        onlyid: row.onlyid,
        is_freeze: !sccc,
        is_lock: row.is_lock,
      };
      this.$store
        .dispatch("management/ManagementStatus", data)
        .then((response) => {
          const { code, msg } = response;
          if (code.toString().substr(0, 1) === "2") {
            row.is_freeze = !sccc;
          }
          this.$message({
            type: code.toString().substr(0, 1) === "2" ? "success" : "error",
            message: msg,
          });
        });
    },
    // 删除
    handleDelete(index, row) {
      if (!row.is_freeze && row.is_confirm) {
        return false;
      }
      let arr1 = [];
      arr1.push({ id: row.id, onlyid: row.onlyid });
      this.$store
        .dispatch("management/DelManagement", JSON.stringify({ data: arr1 }))
        .then((response) => {
          this.pagin.total -= 1;
          this.getAllInfo();
          const { code, msg } = response;
          this.$message({
            type: code.toString().substr(0, 1) === "2" ? "success" : "error",
            message: msg,
          });
        });
    },
    btnBackGround({ row, rowIndex }) {
      if ((row.is_freeze || row.is_lock) &&  !row.is_confirm) {
        return { backgroundColor: "#efe9e8" };
      }
    },
    // ----------- 分页-----------
    // 当前一页显示数量
    handleSizeChange(val) {
      let isR = val * this.pagin.currentPage > this.pagin.total;
      if (isR) {
        this.pagin.pagesize = val;
        this.handleCurrentChange(1);
        return false;
      }
      this.pagin.pagesize = val;
      this.getAllInfo();
    },
    // 当前页码
    handleCurrentChange(val) {
      this.pagin.currentPage = val;
      this.getAllInfo();
    },
  },
  created() {
    this.getAllInfo();
  },
};
</script>
<style scoped>
.dataheader {
  margin-top: 10px;
}
.datamain {
  margin-left: 22px;
}

.timeStyle /deep/ .el-form-item__label,
.timeStyle /deep/ .el-input__inner {
  color: #077bf3;
}

.timeStyle >>> .el-form-item__label,
.timeStyle >>> .el-input__inner {
  color: #077bf3;
}

.secondheader {
  margin-left: 20px;
}

.searchIconStyle {
  margin: auto 0;
}

.amountStyle /deep/ .el-form-item__label,
.amountStyle /deep/ .el-input__inner {
  color: #260fe0;
}
.amountStyle >>> .el-form-item__label,
.amountStyle >>> .el-input__inner {
  color: #260fe0;
}

.totalSumStyle /deep/ .el-input-group__prepend,
.totalSumStyle /deep/ .el-input__inner {
  color: #ca8347;
}
.totalSumStyle >>> .el-input-group__prepend,
.totalSumStyle >>> .el-input__inner {
  color: #ca8347;
}

.freezeStyle {
  background-color: black;
  border: black;
}

.msgheader {
  display: inline-block;
  margin-left: 30px;
}
.msgheader span:nth-child(2) {
  margin-left: 10px;
  color: red;
}
.msgheader span:last-child {
  margin-left: 10px;
}
.btnStyle {
  margin-top: 20px;
  margin-left: 30px;
  vertical-align: middle;
}

.paginationStyle {
  margin-top: 20px;
  margin-left: 30px;
  display: inline-block;
  vertical-align: middle;
}

.btnDelStyle {
  background-color: #f56c6c;
  border-color: #f56c6c;
}

.spstyle {
  margin-right: 61px;
}
</style>
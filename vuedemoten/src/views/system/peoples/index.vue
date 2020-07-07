<template>
  <div id="databox">
    <div class="dataheader">
      <div class="firstheader"></div>
      <!-- 添加及搜索 -->
      <div class="secondheader">
        <el-button @click.native.prevent="addData" type="success" class="addPerStyle">添加用户</el-button>
        <div class="msgsearch">
          <el-input
            type="text"
            class="searchStyle"
            v-model="search"
            size="small"
            placeholder="用户搜索"
            clearable
            @change="serchPutChange"
          ></el-input>
          <el-button
            type="warning"
            icon="el-icon-search"
            size="small"
            @click.native.prevent="btnSearch"
            circle
          ></el-button>
        </div>
      </div>
      <hr />
    </div>
    <div class="datamain">
      <!-- 弹窗对话框  -->
      <el-dialog
        :title="title==='NEW'?'添加用户':'编辑用户'"
        :visible.sync="dialogFormVisible"
        :before-close="handleClose"
      >
        <el-form :model="dialogform" ref="ruleForm" :rules="rules">
          <el-form-item label="用户名称" :label-width="formLabelWidth" prop="username">
            <el-input v-model="dialogform.username" autocomplete="off" clearable></el-input>
          </el-form-item>
          <el-form-item label="用户密码" :label-width="formLabelWidth" prop="password">
            <el-input
              v-model="dialogform.password"
              autocomplete="off"
              :type="passwordStyle"
              clearable
            ></el-input>
            <span class="show-pwd" @click="showPwd">
              <svg-icon :icon-class="passwordStyle==='password'?'eye':'eye-open'" />
            </span>
          </el-form-item>
          <el-form-item label="关联角色" :label-width="formLabelWidth">
            <el-checkbox-group v-model="dialogform.checkedData" >
              <el-checkbox v-for="(one,index) in selectData" :label="one.id" :key="index">{{one.title}}</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native.prevent="cancel">取 消</el-button>
          <el-button type="primary" @click.native.prevent="confirm">确 定</el-button>
        </div>
      </el-dialog>

      <!-- 表格渲染 -->
      <el-table ref="tableForm" :data="tableData" style="width: 100%">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" label="ID" fixed="left"></el-table-column>
        <el-table-column label="角色名称" prop="username" fixed="left"></el-table-column>
        <el-table-column label="关联权限" prop="role">
          <template v-slot="perscope">
            <div>{{ perscope.row.role | filterper }}</div>
          </template>
        </el-table-column>
        <el-table-column align="left" label="编辑" fixed="right">
          <template v-slot="scope">
            <el-button size="mini" @click.native.prevent="handleEdit(scope.$index, scope.row)">Edit</el-button>
            <el-button
              size="mini"
              type="danger"
              @click.native.prevent="handleDelete(scope.$index, scope.row)"
            >Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!-- 分页及按钮 -->
    <div class="datafooter">
      <div class="btnStyle">
        <el-button type="primary" icon="el-icon-share" @click.native.prevent="selectAllData">全选</el-button>
        <el-button
          type="primary"
          icon="el-icon-delete"
          class="btnDelStyle"
          @click.native.prevent="delAllData"
        >全删</el-button>
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
import { sha256 } from "js-sha256";

// 弹窗对话框初始值
const defaultDialogForm = {
  id: "",
  username: "",
  password: "",
  checkedData:[],
};

// 分页初始值
const defaultPagin = {
  currentPage: 1,
  pagesizes: [3, 20, 50],
  pagesize: 3,
  total: 15
};

export default {
  data() {
    return {
      // -----------添加及搜索-----------
      search: "",
      // ----------- 弹窗对话框-----------
      dialogFormVisible: false,
      title: "NEW",
      dialogform: Object.assign({}, defaultDialogForm),
      formLabelWidth: "100px",
      selectData: [],
      
      passwordStyle: "password",
      // ----------- 表格渲染-----------
      tableData: [],
      // ----------- 分页-----------
      pagin: Object.assign({}, defaultPagin),
      // ----------- 验证-----------
      rules: {
        username: [
          { required: true, message: "用户名不能为空", trigger: "blur" },
          { min: 5, max: 32, message: "长度在 5 到 32 个字符", trigger: "blur" }
        ],
        password: [
          { required: true, message: "密码不能为空", trigger: "blur" },
          { min: 6, message: "长度至少6个字符或以上", trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    // -----------添加及搜索-----------
    // 添加目标
    addData() {
      this.title = "NEW";
      this.dialogform = Object.assign({}, defaultDialogForm);
      this.dialogFormVisible = true;
    },
    // 搜索框没有值时触发
    serchPutChange(val) {
      // console.log("666",val)
      let newVal = val.toString().trim();
      if (newVal == "") {
        this.getAllInfo();
      } else {
        return false;
      }
    },
    // 按下搜索时触发
    btnSearch() {
      this.getAllInfo();
    },
    // ----------- 弹窗对话框-----------
    //点击对话框外面事件
    handleClose(done) {
      this.dialogFormVisible = false;
      this.dialogform = Object.assign({}, defaultDialogForm);
      this.$refs["ruleForm"].resetFields();
      done();
    },
    // 确定送出
    confirm() {
      // console.log("---",this.dialogform)
      this.$refs["ruleForm"].validate(val => {
        if (val) {
          this.dialogFormVisible = false;
          let sha256 = require('js-sha256').sha256
          this.dialogform.password = sha256(this.dialogform.password)
          console.log("--", this.dialogform);

          //   this.dialogform.method = this.dialogform.method[0]
          let menuData = JSON.stringify(this.dialogform);
          if (this.title === "EDIT") {
            this.$store.dispatch("peoples/PutUser", menuData).then(response => {
              console.log(response);
              this.getAllInfo();
            });
          } else {
            this.$store.dispatch("peoples/AddUser", menuData).then(response => {
              console.log(response);
              this.getAllInfo();
            });
          }
        }
      });
    },
    // 取消对话框
    cancel() {
      this.dialogFormVisible = false;
      this.dialogform = Object.assign({}, defaultDialogForm);
      this.$refs["ruleForm"].resetFields();
    },
    showPwd() {
      if (this.passwordStyle === "password") {
        this.passwordStyle = "";
      } else {
        this.passwordStyle = "password";
      }
    },

    // ----------- 表格渲染-----------
    // 获取所有目标
    getAllInfo() {
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
        pagesize: this.pagin.pagesize
      };
      if (!!this.search.toString().trim()) {
        // console.log("search", this.search);
        dataInfo["search"] = this.search.toString().trim();
      }
      this.$store.dispatch("peoples/GetUser", dataInfo).then(response => {
        // console.log(response,"***");
        const {data,total} = response
        this.tableData = data;
        this.pagin.total = total;
      });
      this.$store.dispatch("peoples/GetUserRole").then(response => {
        // console.log("dddd", response);
        const { data } = response;
        this.selectData = data;
      });
    },
    // 编辑
    handleEdit(index, row) {
      console.log(row);
      this.dialogform = Object.assign({}, defaultDialogForm);
      this.title = "EDIT";
      this.dialogFormVisible = true;
      this.dialogform.id = row.id;
      this.dialogform.username = row.username;
      let arr1 = [];
      for (let n in row.role) {
        arr1.push(row.role[n].id);
      }
      this.dialogform.checkedData = arr1
    },
    // 删除
    handleDelete(index, row) {
      let arr1 = [];
      arr1.push(row.id);
      this.$store
        .dispatch("peoples/DelUser", JSON.stringify({ id: arr1 }))
        .then(response => {
          // console.log(response);
          this.pagin.total -= 1;
          this.getAllInfo();
        });
    },
    // ----------- 分页-----------
    // 全选
    selectAllData() {
      this.$refs.tableForm.toggleAllSelection();
    },
    // 全删
    delAllData() {
      let arr1 = [];
      const temp = this.$refs.tableForm.selection;
      for (let t in temp) {
        arr1.push(temp[t].id);
        this.pagin.total -= 1;
      }
      this.$store
        .dispatch("peoples/DelUser", JSON.stringify({ id: arr1 }))
        .then(response => {
          this.getAllInfo();
        });
    },
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
    }
  },
  created() {
    this.getAllInfo();
  },
  filters: {
    filterper: function(val) {
      // console.log(val,val.constructor===Array)
      let arr1 = [];
      for (let n in val) {
        arr1.push(val[n].title);
      }
      return arr1.join(",");
    }
  }
};
</script>
<style scoped>
.show-pwd {
  position: absolute;
  right: 30px;
}

.dataheader {
  margin: 10px 0px 0px 20px;
}

.datamain {
  margin-left: 22px;
}

.el-select {
  display: block;
}
.el-button {
  margin-left: 0px;
}
.secondheader {
  margin-left: 10px;
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
  display: inline-block;
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

.searchStyle {
  width: 200px;
  margin-left: 20px;
}

.msgsearch {
  display: inline-block;
}
</style>
<template>
  <div id="databox">
    <div class="dataheader">
      <div class="firstheader"></div>
      <!-- 添加及搜索 -->
      <div class="secondheader">
        <el-form ref="btnForm" :inline="true" class="demo-ruleForm">
          <el-form-item>
            <el-button @click.native.prevent="addData" type="success" class="addPerStyle">添加IP</el-button>
          </el-form-item>
          <el-form-item>
            <el-input
              placeholder="IP搜索"
              v-model.trim="search"
              clearable
              @change="serchPutChange"
              style="width:350px"
            >
              <el-button slot="append" icon="el-icon-search" @click.native.prevent="btnSearch"></el-button>
            </el-input>
          </el-form-item>
          <el-form-item class="btnControlIp">
            <el-switch
                v-model="btnip"
                :active-text="btnip?'IP限制开启':'IP限制关闭'"
                active-color="#13ce66"
                inactive-color="#ff4949"
                @change="btnipevent"
              ></el-switch>
          </el-form-item>
        </el-form>
      </div>
      <hr />
    </div>
    <div class="datamain">
      <!-- 弹窗对话框  -->
      <el-dialog
        :title="title==='NEW'?'添加IP':'编辑IP'"
        :visible.sync="dialogFormVisible"
        :before-close="handleClose"
      >
        <el-form :model="dialogform" ref="ruleForm" :rules="rules">
          <el-form-item label="IP地址" :label-width="formLabelWidth" prop="ip">
            <el-input v-model.trim="dialogform.ip" autocomplete="off" clearable></el-input>
          </el-form-item>
          <el-form-item label="IP状态" :label-width="formLabelWidth" prop="is_through">
            <el-radio v-model="dialogform.is_through" label="1">启用</el-radio>
            <el-radio v-model="dialogform.is_through" label="2">禁用</el-radio>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native.prevent="cancel">取 消</el-button>
          <el-button type="primary" @click.native.prevent="confirm">确 定</el-button>
        </div>
      </el-dialog>

      <!-- 表格渲染 -->
      <el-table ref="tableForm" :data="tableData" style="width: 100%" border>
        <el-table-column type="index" label="ID" fixed="left"></el-table-column>
        <el-table-column label="IP地址" prop="ip" fixed="left"></el-table-column>
        <el-table-column label="状态" prop="is_through" fixed="left">
          <template v-slot="scope">
            <div>{{scope.row.is_through==='2'?"禁用":"启用"}}</div>
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
  ip: "",
  is_through: "2",
};

// 分页初始值
const defaultPagin = {
  currentPage: 1,
  pagesizes: [10, 20, 50],
  pagesize: 10,
  total: 0,
};

export default {
  data() {
    const ipVali = (rule,value,callback) =>{
      const str= value.toString()
      if(str.length===0){
        return callback(new Error("IP地址不能为空"))
      }
      const  reg = /^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$/
      if(!str.match(reg)){
        return callback(new Error("IP地址格式不正确"))
      }
      
      return callback()
    }
    return {
      // -----------添加及搜索-----------
      btnip: false,
      search: "",
      // ----------- 弹窗对话框-----------
      dialogFormVisible: false,
      title: "NEW",
      dialogform: Object.assign({}, defaultDialogForm),
      formLabelWidth: "100px",
      // ----------- 表格渲染-----------
      tableData: [],
      // ----------- 分页-----------
      pagin: Object.assign({}, defaultPagin),
      // ----------- 验证-----------
      rules: {
        ip: [
          { required: true, validator:ipVali, trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    // -----------添加及搜索-----------
    btnipevent(val){
        const btndata = this.btnip?"1":"2"
        this.$store
              .dispatch("whitelist/SetWhitelist", JSON.stringify({"btncontrol":btndata}))
              .then((response) => {
                this.getAllInfo();
                const { code, msg } = response;
                this.$message({
                  type:
                    code.toString().substr(0, 1) === "2" ? "success" : "error",
                  message: msg,
                });
        });
    },
    // 添加目标
    addData() {
      this.title = "NEW";
      this.dialogform = Object.assign({}, defaultDialogForm);
      this.dialogFormVisible = true;
    },
    // 搜索框没有值时触发
    serchPutChange(val) {
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
      this.$refs["ruleForm"].validate((val) => {
        if (val) {
          this.dialogFormVisible = false;
          let whiteData = JSON.stringify(this.dialogform);
          if (this.title === "EDIT") {
            this.$store
              .dispatch("whitelist/PutWhitelist", whiteData)
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
              .dispatch("whitelist/AddWhitelist", whiteData)
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
      this.dialogform = Object.assign({}, defaultDialogForm);
      this.$refs["ruleForm"].resetFields();
    },

    // ----------- 表格渲染-----------
    // 获取所有目标
    getAllInfo() {
      // this.pagin = Object.assign({},defaultPagin)
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
      if (!!this.search.toString().trim()) {
        dataInfo["search"] = this.search.toString().trim();
        // 有搜索需要恢复初始值，否则会显示错误
        dataInfo["currentpage"] = 1;
        this.pagin.currentPage = 1;
      }
      this.$store
        .dispatch("whitelist/GetWhitelist", dataInfo)
        .then((response) => {
          this.tableData = response.data;
          this.pagin.total = response.total;
          this.btnip = response.is_global;
        });
    },
    // 编辑
    handleEdit(index, row) {
      this.dialogform = Object.assign({}, defaultDialogForm);
      this.title = "EDIT";
      this.dialogFormVisible = true;
      this.dialogform.id = row.id;
      this.dialogform.ip = row.ip;
      this.dialogform.is_through = row.is_through;
    },
    // 删除
    handleDelete(index, row) {
      let arr1 = [];
      arr1.push(row.id);
      this.$store
        .dispatch("whitelist/DelWhitelist", JSON.stringify({ id: arr1 }))
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
.treeStyle {
  margin-top: 7px;
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

.btnControlIp {
    border: 1px solid #DCDFE6;
    padding: 0 5px 0 5px;
    border-radius: 4px;
}
</style>
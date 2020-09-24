from flask import *
from flask_sqlalchemy import SQLAlchemy
from mypj import predict

app = Flask(__name__)
app.secret_key = '84375r0hfuggwkjvgfjhvsjhgv'


# 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3307/test'
# 动态追踪修改设置，如未设置只会提示警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128), nullable=False)

class applylist(db.Model):
    __tablename__ = 'applylist'
    ID = db.Column(db.Integer, primary_key=True)
    Gender = db.Column(db.String(128), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Debt = db.Column(db.DECIMAL(20,6), nullable=False)
    Married = db.Column(db.String(128), nullable=False)
    BankCustomer = db.Column(db.String(128), nullable=False)
    EducationLevel = db.Column(db.String(128), nullable=False)
    Ethnicity = db.Column(db.String(128), nullable=False)
    YearsEmployed = db.Column(db.Integer, nullable=False)
    PriorDefault = db.Column(db.String(128), nullable=False)
    Employed = db.Column(db.String(128), nullable=False)
    CreditScore = db.Column(db.Integer, nullable=False)
    DriversLicense = db.Column(db.String(128), nullable=False)
    Citizen = db.Column(db.String(128), nullable=False)
    ZipCode = db.Column(db.String(128), nullable=True)
    Income = db.Column(db.Integer, nullable=False)
    ApprovalStatus = db.Column(db.String(128), nullable=False)

@app.route('/init')
def init():
    # db.create_all()
    return 'ok'

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('ind'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        if all([user, pwd]):
            a = User.query.filter(User.id == user).first()
            if a:
                # 如果用户存在，判断密码是否正确
                if a.password == pwd:
                    # 登录成功后，session['admin_id']存入数据，
                    # 其他页面用来判断用户到登录状态
                    session['admin_id'] = a.id
                    session['logged_in'] = True
                    flash('登陆成功')
                    # 登录成功后跳转到首页
                    return redirect(url_for('ind'))
                else:
                    flash('密码错误')
            else:
                flash('用户名不存在')
        else:
            flash('用户名、密码不完整')
    return render_template('login.html')


@app.route('/user', methods=['GET', 'POST'])
def ind():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        gender = request.form.get('sex')
        age = request.form.get('Age')
        Debt = request.form.get('Debt')
        married = request.form.get('married')
        bank = request.form.get('bank')
        edu = request.form.get('edu')
        ethnicity = request.form.get('ethnicity')
        YearsEmployed = request.form.get('YearsEmployed')
        priordefault = request.form.get('priordefault')
        employed = request.form.get('employed')
        CreditScore = request.form.get('CreditScore')
        driverslicense = request.form.get('driverslicense')
        citizen = request.form.get('citizen')
        ZipCode = request.form.get('ZipCode')
        Inomec = request.form.get('Income')
        #后台数据处理
        if all([age, Debt, YearsEmployed, Inomec, CreditScore]):
            if(age.isdigit()):
                if(Debt.isdigit()):
                    if(YearsEmployed.isdigit()):
                        if(Inomec.isdigit()):
                            if(CreditScore.isdigit()):
                                test = [int(gender), int(age), int(Debt), int(married), int(bank), int(edu),
                                        int(ethnicity),
                                        int(YearsEmployed),
                                        int(priordefault),
                                        int(employed),
                                        int(CreditScore),
                                        int(driverslicense), int(citizen), int(ZipCode), int(Inomec)
                                        ]
                                result = predict(test)
                                if(result == 0):
                                    flash('预测结果：申请成功！')
                                else:
                                    flash('预测结果：申请失败')
                                load_to_db(test, result)
                            else:
                                flash('提示：请正确输入信用评分！')
                        else:
                            flash('提示：请正确输入收入情况！')
                    else:
                        flash('提示：请正确输入录用年数！')
                else:
                    flash('提示：请正确输入负债金额！')
            else:
                flash('提示：请正确输入年龄！')
        else:
            flash('提示：请不要空缺信息！')
    return render_template('test.html')

def load_to_db(test,result):
    alist = applylist()
    print(test)

    if test[0] == 0:
        alist.Gender = '男'
    else:
        alist.Gender = '女'
    alist.Age = test[1]
    alist.Debt = test[2]

    if test[3] == 0:
        alist.Married = '未婚'
    elif test[3] == 1:
        alist.Married = '已婚'
    elif test[3] == 2:
        alist.Married = '丧偶'
    elif test[3] == 3:
        alist.Married = '离婚'

    if test[4] == 0:
        alist.BankCustomer = '普通会员'
    elif test[4] == 1:
        alist.BankCustomer = 'VIP会员'
    elif test[4] == 2:
        alist.BankCustomer = '金卡会员'

    if test[5] == 0:
        alist.EducationLevel = '小学以下'
    elif test[5] == 1:
        alist.EducationLevel = '小学'
    elif test[5] == 2:
        alist.EducationLevel = '初中'
    elif test[5] == 3:
        alist.EducationLevel = '高中'
    elif test[5] == 4:
        alist.EducationLevel = '中专'
    elif test[5] == 5:
        alist.EducationLevel = '大专'
    elif test[5] == 6:
        alist.EducationLevel = '本科'
    elif test[5] == 7:
        alist.EducationLevel = '硕士研究生'
    elif test[5] == 8:
        alist.EducationLevel = '博士研究生'
    elif test[5] == 9:
        alist.EducationLevel = '博士后'

    if test[6] == 0:
        alist.Ethnicity = '汉族'
    elif test[6] == 1:
        alist.Ethnicity = '壮族'
    elif test[6] == 2:
        alist.Ethnicity = '回族'
    elif test[6] == 3:
        alist.Ethnicity = '满族'
    elif test[6] == 4:
        alist.Ethnicity = '维吾尔族'
    elif test[6] == 5:
        alist.Ethnicity = '苗族'
    elif test[6] == 6:
        alist.Ethnicity = '彝族'
    elif test[6] == 7:
        alist.Ethnicity = '土家族'
    elif test[6] == 8:
        alist.Ethnicity = '其他'

    alist.YearsEmployed = test[7]

    if test[8] == 0:
        alist.PriorDefault = '有'
    else:
        alist.PriorDefault = '无'

    if test[9] == 0:
        alist.Employed = '是'
    else:
        alist.Employed = '否'

    alist.CreditScore = test[10]

    if test[11] == 0:
        alist.DriversLicense = '有'
    else:
        alist.DriversLicense = '无'

    if test[12] == 0:
        alist.Citizen = '农村户口'
    elif test[12] == 1:
        alist.Citizen = '城市户口'
    elif test[12] == 2:
        alist.Citizen = '外国人永久居留'

    alist.ZipCode = test[13]

    alist.Income = test[14]

    if result == 0:
        alist.ApprovalStatus = '成功'
    else:
        alist.ApprovalStatus = '失败'

    db.session.add(alist)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)

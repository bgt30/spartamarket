~~디렉토리 이동하다 git 오류가 났는데 뭘 해도 해결이 안됐습니다.. 결국 git init 해서 commit 내역이 거의 없습니다..~~

# Sparta Market

## 📝 프로젝트 소개
중고 거래 플랫폼 웹 애플리케이션입니다. Django를 활용하여 사용자들이 상품을 등록하고, 검색하며, 소통할 수 있는 기능을 제공합니다.

## ⚙️ 개발 환경
- **Language**: `Python 3.10.11`
- **Framework**: `Django 4.2`
- **Database**: `SQLite`
- **IDE**: `Visual Studio Code`

## 📌 주요 기능

### 1. 사용자 관리 (Accounts)
#### 1.1 회원가입/로그인
- 이메일, 사용자명, 비밀번호를 통한 회원가입
- Django Auth를 활용한 로그인/로그아웃
- 로그인 상태에 따른 접근 권한 제어

#### 1.2 프로필 관리
- 프로필 이미지 업로드/수정 기능
- 기본 프로필 이미지 제공 (user.png)
- 팔로우/언팔로우 기능
- 팔로워/팔로잉 수 표시

### 2. 상품 관리 (Products)
#### 2.1 상품 CRUD
- 상품 등록: 제목, 설명, 해시태그 입력
- 상품 수정/삭제: 작성자 본인만 가능
- 상품 조회: 모든 사용자 가능

#### 2.2 상품 목록
- 최신순/인기순 정렬 기능
- 통합 검색 기능 (제목, 설명, 작성자, 해시태그)
- 페이지당 12개 상품 표시

#### 2.3 상품 상세
- 조회수 자동 증가
- 찜하기 기능
- 해시태그 표시
- 작성자 프로필 링크

### 3. 해시태그 시스템
- 상품별 다중 해시태그 등록
- 특수문자, 공백 제한
- 중복 해시태그 자동 처리
- 해시태그 기반 검색

## 💾 DB 설계
### User 모델
```python
class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
```

### Product 모델
```python
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_products')
    view_count = models.IntegerField(default=0)
    hashtags = models.ManyToManyField('Hashtag', blank=True)
```

### Hashtag 모델
```python
class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
```

## 📁 프로젝트 구조
```
spartamarket/
├── accounts/                 # 사용자 관리 앱
│   ├── models.py            # User 모델
│   ├── views.py             # 로그인, 회원가입, 프로필 관련 뷰
│   └── templates/           # 사용자 관련 템플릿
├── products/                # 상품 관리 앱
│   ├── models.py            # Product, Hashtag 모델
│   ├── views.py             # 상품 CRUD 관련 뷰
│   └── templates/           # 상품 관련 템플릿
├── templates/               # 공통 템플릿
│   ├── base.html           # 기본 템플릿
│   └── home.html           # 홈페이지
├── media/                   # 미디어 파일 저장
│   └── profile_images/     # 프로필 이미지
└── spartamarket/           # 프로젝트 설정
    ├── settings.py
    └── urls.py
```

## 🔍 Views 상세 설명
### 1. 상품 검색 및 정렬
```python
def product_list(request):
    sort = request.GET.get('sort', '-created_at')
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(owner__username__icontains=query) |
            Q(hashtags__name__icontains=query)
        ).distinct()
    else:
        products = Product.objects.all()
    
    if sort == 'popular':
        products = products.annotate(
            like_count=Count('likes')
        ).order_by('-like_count', '-created_at')
    else:
        products = products.order_by('-created_at')
```

### 2. 팔로우 기능
```python
@login_required
def follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if request.user != target_user:
        if request.user.following.filter(id=target_user.id).exists():
            request.user.following.remove(target_user)
        else:
            request.user.following.add(target_user)
    
    return redirect('accounts:profile', user_id=user_id)
```

## 📡 API 명세

### 1. 사용자 관리 (Accounts)

| 기능 | Method | URL | Request | Response |
|------|--------|-----|---------|-----------|
| 회원가입 | POST | `/accounts/signup/` | ```json { "username": "string", "email": "user@example.com", "password1": "string", "password2": "string" }``` | 성공 시 로그인 페이지로 리다이렉트 |
| 로그인 | POST | `/accounts/login/` | ```json { "username": "string", "password": "string" }``` | 성공 시 메인 페이지로 리다이렉트 |
| 프로필 조회 | GET | `/accounts/profile/<int:user_id>/` | - | 프로필 페이지 렌더링 |
| 프로필 수정 | POST | `/accounts/profile/update/` | `multipart/form-data` ```json { "profile_image": "file" }``` | 성공 시 프로필 페이지로 리다이렉트 |
| 팔로우/언팔로우 | POST | `/accounts/profile/<int:user_id>/follow/` | - | 성공 시 프로필 페이지로 리다이렉트 |

### 2. 상품 관리 (Products)

| 기능 | Method | URL | Request | Response |
|------|--------|-----|---------|-----------|
| 상품 목록 조회 | GET | `/products/` | Query Parameters: `sort`: `-created_at` 또는 `popular`, `q`: 검색어 | 상품 목록 페이지 렌더링 |
| 상품 상세 조회 | GET | `/products/<int:product_id>/` | - | 상품 상세 페이지 렌더링 |
| 상품 등록 | POST | `/products/create/` | ```json { "title": "string", "description": "string", "hashtags": "string" }``` | 성공 시 상품 상세 페이지로 리다이렉트 |
| 상품 수정 | POST | `/products/<int:product_id>/update/` | ```json { "title": "string", "description": "string", "hashtags": "string" }``` | 성공 시 상품 상세 페이지로 리다이렉트 |
| 상품 삭제 | POST | `/products/<int:product_id>/delete/` | - | 성공 시 상품 목록 페이지로 리다이렉트 |
| 상품 찜하기/취소 | POST | `/products/<int:product_id>/like/` | - | 성공 시 상품 상세 페이지로 리다이렉트 |

### 3. 응답 코드

| 코드 | 설명 |
|------|------|
| 200 | 성공 |
| 201 | 생성 성공 |
| 400 | 잘못된 요청 |
| 401 | 인증 필요 |
| 403 | 권한 없음 |
| 404 | 리소스 없음 |
| 500 | 서버 오류 |

### 4. 인증
- 대부분의 API는 로그인이 필요합니다
- 인증되지 않은 요청은 로그인 페이지로 리다이렉트됩니다
- Django의 세션 기반 인증을 사용합니다

## 🚀 시작하기

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/sparta_market.git
cd sparta_market
```

### 2. 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 데이터베이스 설정
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 서버 실행
```bash
python manage.py runserver
```

## 📜 라이센스
This project is licensed under the MIT License
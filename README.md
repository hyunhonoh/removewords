# removewords

Splunk에 들어가 있는 이벤트 중에서 반복되면서 삭제 태그를 달고 싶을 때 비교문을 이용해서 삭제 태그를 달 수 있게 해주는 커스텀 명령어



- 사용예

```
index="txt" 
| removewords body
| table body, removewords
```


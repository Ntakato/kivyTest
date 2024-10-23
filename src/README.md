# sync_sample.py

kivyの公式が提示しているasyncサンプル

https://github.com/kivy/kivy/blob/master/examples/async/asyncio_advanced.py

非同期処理をkivyで処理するための処理の解説

```python
    def app_func(self):
        '''This will run both methods asynchronously and then block until they
        are finished
        '''
        self.other_task = asyncio.ensure_future(self.waste_time_freely())

        async def run_wrapper():
            # we don't actually need to set asyncio as the lib because it is
            # the default, but it doesn't hurt to be explicit
            await self.async_run(async_lib='asyncio')
            print('App done')
            self.other_task.cancel()

        return asyncio.gather(run_wrapper(), self.other_task)
```

`asyncio.ensure_future(self.waste_time_freely())` でwaste_time_freelyをタスクとして定義

run_wrapperはkivyアプリケーションを実行するラッパー
`async_run()`は`run()`と同じだが、コルーチンであり、非同期イベントループ内でスケジュールできる  
https://kivy.org/doc/stable/api-kivy.app.html#kivy.app.App.async_run  

ここではkivyアプリをコルーチンとして実行して、kivyアプリが終了したらother_taskもcancelして終了するようにラップしている

`return asyncio.gather(run_wrapper(), self.other_task)`でラップしたkivyアプリと非同期処理waste_time_freelyをイベントループの中で走らせる

```python
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(AsyncApp().app_func())
    loop.close()
```

https://kivy.org/doc/stable/api-kivy.app.html#asynchronous-app  
の内容  
AsyncAppインスタンスを作成し、非同期イベントループを実行する  
run_until_completeでapp_funcを実行し、アプリケーションが終了するまで待機する

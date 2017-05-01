import React from 'react';
import { Layout } from 'antd';
import styles from './MainLayout.css';
import HeaderContent from './HeaderCont';
import SiderContent from './SiderCont';

const { Header, Content, Sider, Footer } = Layout;

function MainLayout({ children, location }) {
  return (
    <Layout style={{ height: '100%' }}>
      <Header className="header">
        <div className={styles.logo} >
          <a className={styles.logo_txt} >QTPweb接口测试系统</a>
        </div>
        <HeaderContent location={location} />
      </Header>
      <Layout >
        <Sider width={200} style={{ background: '#fff' }}>
          <SiderContent />
        </Sider>
        <Layout>
          <Content style={{ background: '#fff', padding: 24, margin: 0, minHeight: 280 }}>
            <div className={styles.content}>
              <div className={styles.main}>
                {children}
              </div>
            </div>
          </Content>
        </Layout>
      </Layout>
      <Footer style={{ textAlign: 'center' }}>
        Ant Design ©2016 Created by Ant UED
      </Footer>
    </Layout>);
}

export default MainLayout;


import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Documentation Focused',
    Svg: require('@site/static/img/undraw_contract_ynau.svg').default,
    description: (
      <>
        Create and manage well-structured documentation with ease. Designed for developers and teams who want a fast, organized, and scalable documentation experience.
      </>
    ),
  },
  {
    title: 'Documnent Search',
    Svg: require('@site/static/img/undraw_document-search_2o7x.svg').default,
    description: (
      <>
        Quickly find the information you need with powerful and intelligent search capabilities that make navigating large documentation effortless.
      </>
    ),
  },
  {
    title: 'Document Analysis',
    Svg: require('@site/static/img/undraw_document-analysis_3c0y.svg').default,
    description: (
      <>
        Analyze, customize, and extend your documentation platform with flexible components and modern tools for a smarter user experience.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4 gap--md ')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
